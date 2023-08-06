#ifndef _JIT_HOST_H_
#define _JIT_HOST_H_

#include <vector>

#if (WIN32)
#define JIT_EXPORT __declspec(dllexport) 
#else
#define JIT_EXPORT
#endif

//all funcation,if return GalaxyJitPtr will hold a new reference
typedef void* GalaxyJitPtr;
class JitHost
{
public:
	virtual void AddFunc(void* context, const char* hash,const char* funcName, void* funcPtr) = 0;
	virtual int to_int(GalaxyJitPtr pVar) = 0;
	virtual GalaxyJitPtr from_int(int val) = 0;
	virtual long long to_longlong(GalaxyJitPtr pVar) = 0;
	virtual GalaxyJitPtr from_longlong(long long val) = 0;
	virtual float to_float(GalaxyJitPtr pVar) = 0;
	virtual GalaxyJitPtr from_float(float val) = 0;
	virtual const char* to_str(GalaxyJitPtr pVar) = 0;
	virtual GalaxyJitPtr from_str(const char* val) = 0;

	virtual int GetCount(GalaxyJitPtr objs) = 0;
	virtual GalaxyJitPtr Get(GalaxyJitPtr objs, int idx) = 0;
	virtual int Set(GalaxyJitPtr objs, int idx, GalaxyJitPtr val) = 0;
	virtual GalaxyJitPtr Get(GalaxyJitPtr objs, const char* key) = 0;
	virtual bool ContainKey(GalaxyJitPtr container, GalaxyJitPtr key) = 0;
	virtual bool KVSet(GalaxyJitPtr container, GalaxyJitPtr key, GalaxyJitPtr val) = 0;
	virtual void Free(const char* sz) = 0;
	virtual int AddRef(GalaxyJitPtr obj) = 0;
	virtual void Release(GalaxyJitPtr obj) = 0;
	virtual GalaxyJitPtr Call(GalaxyJitPtr obj, int argNum, GalaxyJitPtr* args) = 0;
	virtual GalaxyJitPtr Call(GalaxyJitPtr obj, int argNum, GalaxyJitPtr* args, GalaxyJitPtr kwargs) = 0;
	virtual GalaxyJitPtr NewList(long long size) = 0;
	virtual GalaxyJitPtr NewDict() = 0;
	virtual GalaxyJitPtr NewArray(int nd, unsigned long long* dims, int itemDataType) = 0;
	virtual void* GetDataPtr(GalaxyJitPtr obj) = 0;
	virtual bool GetDataDesc(GalaxyJitPtr obj, 
		int& itemDataType,
		std::vector<unsigned long long>& dims,
		std::vector<unsigned long long>& strides) = 0;
	virtual GalaxyJitPtr Import(const char* key) = 0;
};

#endif//_JIT_HOST_H_

