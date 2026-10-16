# 2.4.3 function map (identified so far)

Addresses identified from `Wow.exe` 2.4.3.8606 by disassembly + string/import evidence,
cross-referenced with the 3.3.5a source. Confidence is how sure the *name/module* is, not the body.

## Os module

| Address | Name | Evidence | Confidence |
|---|---|---|---|
| `0x00749F00` | `CreateNamedEventA` | called by `0x00402CF0` with the event-name string; declared in 3.3.5a `Os/System.h` | high |
| `0x00749F20` | `ProtectProcessSecurity` | DACL hardening; adjacent to `CreateNamedEventA` | high |
| `0x00749A60` | `OsSystemEnableCpuLog` | called from `CommonMain` | medium |
| `0x0074A900` | `GetExecutablePathUTF8` | fills a 1560-byte path buffer in `SetInstallPath` | high |

## Storm module

| Address | Name | Evidence | Confidence |
|---|---|---|---|
| `0x00643140` | `SMem` static `FatalError` | `"Requested %u bytes of memory"` | high |
| `0x006441F0` | `SMemAlloc` | called by `operator new` (0x401010) | high |
| `0x00644230` | `SMemFree` | called by `operator delete[]` (0x401030) | high |
| `0x006448FC*` | `SMemSetDebugFlags`/... | (SMem cluster around 0x643xxx) | low |
| `0x00648FB0` | `StormInitialize` | first call in `CommonMain` | medium |
| `0x00648FC0` | `StormDestroy` | last call in `CommonMain` | medium |
| `0x00649040` | `StormSetOption` | `CommonMain` calls it with `(10/11, &option, 4)` | high |
| `0x00647FF0` | `SErrCatchUnhandledExceptions` | 2nd call in `CommonMain` | medium |
| `0x00647030` | `SErrSetLogTitleString` | `CommonMain` passes the "build 8606" title | high |
| `0x00647070` | `SErrSetLogCallback` | `CommonMain` passes `WowLogHeader` (0x4040B0) | high |
| `0x00647250` | `SErrRegisterHandler` | `CommonMain` passes `SendErrorLog` (0x402BF0) | high |
| `0x00645EB0` | `SRegLoadValue` | `CommonMain` ("World of Warcraft\\Client","SendErrorLogs") | high |
| `0x00646050` | `SRegSaveValue` | `CommonMain` failure path | high |
| `0x00644A10` | `SStrChrR` | `SetInstallPath` scans for the trailing `\\` | high |
| `0x00645D60` | `SRegLoadString` | `SetInstallPath` load | high |
| `0x00645F80` | `SRegSaveString` | `SetInstallPath` save | high |
| `0x00644A90` | string/path compare | `SetInstallPath` (`0x7FFFFFFF` max length) | low |

## Operators and Client

| Address | Name | Evidence | Confidence |
|---|---|---|---|
| `0x00401010` | `operator new` | `SMemAlloc(bytes, "new", -1, 0)`; matches 3.3.5a OFFSET 0x401010 | high |
| `0x00401030` | `operator delete[]` | `SMemFree(ptr, "delete[]", -1, 0)`; matches 3.3.5a OFFSET 0x401030 | high |
| `0x0047CC90` | `operator delete` *(3.3.5a address)* | **not** at this address in 2.4.3 — still to locate | n/a |
| `0x00402CF0` | named-event wrapper | `CreateNamedEventA("Blizzard Entertainment World of Warcraft", 0)` | high |

`SLOG_FUNCTION` is `-1` in 2.4.3 (the `__LINE__` slot), confirmed in the operators.

## Storm allocator (2.4.3 design difference)

`SMemAlloc`/`SMemFree` do **not** call `malloc`/`calloc` directly as in 3.3.5a. They delegate to an
allocator object:

| Address | Role |
|---|---|
| `0x00D73700` | the allocator instance (the `this` pointer both methods receive in `ecx`) |
| `0x00644090` | `allocator::Alloc(bytes, filename, linenumber)` — called by `SMemAlloc` |
| `0x00644190` | `allocator::Free(ptr, filename, linenumber)` — called by `SMemFree` |

`SMemAlloc` then zeroes the block with `memset` (0x0040A620) when `flags & SMEM_FLAG_ZEROMEMORY`.

## Storm heap layout (from the disassembly)

`SHeap` (0x00D73700) is a size-classed free-list allocator:

| Offset | Field |
|---|---|
| `+0x00C` | bin descriptors, 16 bytes each: `bin[sizeClass]` |
| `+0x20C` | free-list heads, 4 bytes each: `head[index]` |
| `+0x40C` | statistic (bytes in use; `ReleaseBlock` subtracts) |
| `+0x410` | statistic (`ReleaseBlock` subtracts the block size) |
| `+0x414` | statistic (`ReleaseBlock` adds `size - (1<<class) + 8`) |
| `+0x424` | enabled flag (checked by `Alloc`/`Free`) |
| `+0x42C` | `CRITICAL_SECTION` guarding the bins |

Allocation header (8 bytes): word 0 bit 0 = allocated, bits 1..7 = free-list index; word 1 bits 0..4
= size class.

Ported so far in `Engine/Source/Storm/Source/SMem.cpp`: `Alloc` (0x00644090), `Free` (0x00644190),
`GetSizeClass` (0x006434A0, = `max(3, ceil(log2(bytes + 8)))`), `FatalError` (0x00643140),
`SMemAlloc`/`SMemFree`, the global operators. Still to port:

| Address | Role |
|---|---|
| `0x00643A20` | `AllocateBlock(sizeClass, bytes, unk)` — splits from `bin[class]` (16-byte stride) or recurses a class up; calls `0x006432B0`, `0x006438F0` |
| `0x00643680` | `ValidateBlock(block, ...)` — `IsBadReadPtr`, header checks, free-list membership; `STORM_ERROR_MEM_INVALID` (0x8510007C) via `0x00643110` |
| `0x00643F00` | `ReleaseBlock(block)` — unlinks from `bin[class]`, updates the stats at +0x40C/+0x410/+0x414; calls `0x00643530` |
| `0x00643210` | membership test: block must be within `[head, head + 0x1000000)` and aligned to its size class |
| `0x00643530` | computes a sibling/buddy index (`node + ((block - node) ^ (1 << class))`) |
| `0x00643110` | Storm error report (`STORM_ERROR_MEM_INVALID`) |

The per-class free lists are **binary heaps**, not plain linked lists: `0x006438F0` removes an element
from the heap array and sifts up (`0x006432C0`), keyed by block size. So the heap is a size-classed
heap-ordered free-list allocator (buddy-like indexing via XOR). Reconstructing it faithfully needs
IDA types/xrefs; the interlocking set is `0x00643A20` (allocate/split), `0x006438F0`/`0x006432C0`
(heap remove/sift), `0x006432B0` (head), `0x00643210` (membership), `0x00643530` (buddy index).

`ValidateBlock`'s tail also tests a heap-integrity word at `this+4` against the block pointer; its
exact meaning needs IDA. This allocator's bin-list methods are the next subsystem to reconstruct.

## Caveat: 2.4.3 Storm API signatures differ from 3.3.5a

The headers ported from 3.3.5a (`H/Types.h`, `H/storm.h`) are a starting point, **not** authoritative
for 2.4.3. Example: `SErrDisplayError` takes **6** arguments in 2.4.3 (FatalError at 0x00643140
pushes `errorcode, filename, linenumber, description, recoverable, exitcode`) but **7** in 3.3.5a
(the extra `0x11111111`). Likewise 2.4.3's `FatalError` calls `StormExitProcess(1)` unconditionally,
with no `s_exitonfailure` check. API signatures must be confirmed against the 2.4.3 binary (IDA)
before the headers are trusted.

## Notes

- The `0x0064xxxx` and `0x0074xxxx` clusters are Storm and Os respectively; `CreateNamedEventA`
  (0x749F00) and `ProtectProcessSecurity` (0x749F20) are adjacent in the **Os** module, so
  `ProtectProcessSecurity` should move out of `WinMain.cpp` into the Os module when it is ported.
- Names marked medium/low are carried from the 3.3.5a position; confirm with IDA before relying on
  them.
