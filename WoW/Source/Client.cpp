#include "WoW/Source/Client.h"

// Reconstructed from Wow.exe 2.4.3.8606, 0x00406790. The call sequence matches the 3.3.5a
// CommonMain; the string arguments are confirmed against the binary (the registry path and value
// name at 0x0088BB3C / 0x0088D2B8, the log title at 0x0088D298). Callee names are carried from the
// 3.3.5a equivalents and still need per-function verification.
//
// OFFSET: 0x00406790
int32_t CommonMain() {
    StormInitialize();
    SErrCatchUnhandledExceptions();
    CreateNamedEventA("Blizzard Entertainment World of Warcraft", 0);

    int32_t option = 1;
    StormSetOption(10, &option, sizeof(option));
    option = 1;
    StormSetOption(11, &option, sizeof(option));

    OsSystemEnableCpuLog();
    SetPaths();

    uint32_t sendErrorLogs = 1;

    if (!SRegLoadValue("World of Warcraft\\Client", "SendErrorLogs", 0, &sendErrorLogs)) {
        sendErrorLogs = 1;
        SRegSaveValue("World of Warcraft\\Client", "SendErrorLogs", 0, 1);
    }

    SErrSetLogTitleString("World of WarCraft (build 8606)");
    SErrSetLogCallback(WowLogHeader);

    if (sendErrorLogs) {
        SErrRegisterHandler(SendErrorLog);
    }

    // TODO: 2.4.3 runs this block here (raw addresses from 0x0040682A; see re/243/entry_functions.md).
    //   if (!sub_65A3F0() && !sub_402460())    // 0x65A3F0 returns false; 0x402460 reads g_0xBDB208 == 2
    //       SetInstallPath();                   // 0x402C40 (3.3.5a Client.cpp:815)
    //   if (sub_4063B0()) {                     // big init: CmdLineProcess + CVar registration
    //       if (sub_667090())                   // always true
    //           sub_427E80();                   // thunk -> 0x429D50 (subsystem reset)
    //       sub_405E50();                       // large teardown sequence (BeginCloseGame?)
    //   }
    // The game loop (3.3.5a EventDoMessageLoop) has not been located; port this block before the
    // client can run.

    StormDestroy();

    return 0;
}
