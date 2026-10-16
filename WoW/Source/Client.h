#ifndef WOW_SOURCE_CLIENT_H
#define WOW_SOURCE_CLIENT_H

#include <cstdint>
#include "Engine/Source/Storm/H/storm.h"

// Partial header: only what has been ported so far. The rest of the Client module lands with its
// own functions.

int32_t CommonMain();

int32_t STORMAPI SendErrorLog(uint32_t errorcode, const char* description, const char* filename, int32_t linenumber, const char* errorstring);
int32_t STORMAPI WowLogHeader(char* buffer, uint32_t bufferchars);

#endif
