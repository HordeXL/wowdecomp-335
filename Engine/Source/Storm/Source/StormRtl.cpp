#include "Engine/Source/Storm/H/storm.h"

// OFFSET: 0x00643000
void StormRtlDestroy() {
    SErrSetLogCallback(nullptr);
    SMemDestroy();
    SErrDestroy();
    SLogDestroy();
}

// OFFSET: 0x00643020
void StormRtlInitialize() {
    SLogInitialize();
    SMemInitialize();
}
