#pragma once
#include <stdlib.h>

class VxScratch {
	public:
	VxScratch(size_t iSize = 0);
	~VxScratch();
	void* Check(size_t iSize);
	void* Mem();

	// the memory
	void* m_Memory;

	VxScratch(const VxScratch&);
	VxScratch& operator=(const VxScratch&);

};