#ifndef _JIT_OBJECT_H_
#define _JIT_OBJECT_H_

#include <string>
#include <vector>
#include <map>
#include <unordered_map>
#include "Jit_Host.h"

extern JitHost* g_pHost;

template<class TBase>
class JitObjectRef
{
	enum class IndexType
	{
		Index,
		KEY
	};
public:
	JitObjectRef(TBase p, const char* key)
	{
		m_p = p;
		m_key = key;
		m_idxType = IndexType::KEY;
	}
	JitObjectRef(TBase p, int index)
	{
		m_p = p;
		m_index = index;
		m_idxType = IndexType::Index;
	}
	inline JitObjectRef<TBase> operator[](const char* key)
	{
		return TBase(*this).operator[](key);
	}
	template<class TFrom>
	void operator = (TFrom v)
	{
		if (m_idxType == IndexType::KEY)
		{
			g_pHost->KVSet(m_p,(TBase)m_key, (TBase)v);
		}
		else if (m_idxType == IndexType::Index)
		{
			g_pHost->Set(m_p,m_index, (TBase)v);
		}
	}
	template<typename TC>
	explicit operator TC /*const*/ () const//todo:c++17 can't take this 
	{
		if (m_idxType == IndexType::KEY)
		{
			return (TC)(TBase)g_pHost->Get(m_p, m_key.c_str());
		}
		else if (m_idxType == IndexType::Index)
		{
			return (TC)(TBase)g_pHost->Get(m_p,m_index);
		}
		else
		{
			return 0;
		}
	}
	template<typename... VarList>
	TBase operator()(VarList... args)
	{
		GalaxyJitPtr* ptrs = nullptr;
		const int size = sizeof...(args);
		TBase objs[size] = { args... };
		ptrs = new GalaxyJitPtr[size];
		for (int i = 0; i < size; i++)
		{
			ptrs[i] = objs[i];
		}
		//ptrs will be deleted by .Call
		return TBase(*this).Call(size, ptrs);
	}
	TBase operator()()
	{
		return TBase(*this).Call(0, nullptr);
	}
protected:
	TBase m_p;
	IndexType m_idxType = IndexType::Index;
	std::string m_key;
	int m_index=0;
};

//copy from C:\Python38\Lib\site-packages\numpy\core\include\numpy\ndarraytypes.h
enum class JIT_DATA_TYPES
{
	BOOL = 0,
	BYTE, UBYTE,
	SHORT, USHORT,
	INT, UINT,
	LONG, ULONG,
	LONGLONG, ULONGLONG,
	FLOAT, DOUBLE, LONGDOUBLE,
	CFLOAT, CDOUBLE, CLONGDOUBLE,
	OBJECT = 17,
	STRING, _UNICODE_,
	VOIDTYPE,
	DATAFRAME,//for DataFrame
};
class JitObject
{
public:
	JitObject()
	{

	}
	static JitObject Import(const char* moduleName)
	{
		return JitObject(g_pHost->Import(moduleName));
	}
	template <typename VALUE>
	JitObject(std::vector<VALUE> li)
	{
		m_p = g_pHost->NewList(li.size());
		for (int i=0;i<(int)li.size();i++)
		{
			g_pHost->Set(m_p,i,(JitObject)li[i]);
		}
	}
	template <typename KEY, typename VALUE>
	JitObject(std::map <KEY, VALUE> kvMap)
	{
		m_p = g_pHost->NewDict();
		for (auto kv : kvMap)
		{
			g_pHost->KVSet(m_p,(JitObject)kv.first,(JitObject)kv.second);
		}
	}
	template <typename KEY, typename VALUE>
	JitObject(std::unordered_map <KEY, VALUE> kvMap)
	{
		m_p = g_pHost->NewDict();
		for (auto kv : kvMap)
		{
			g_pHost->Set(m_p, (JitObject)kv.first, (JitObject)kv.second);
		}
	}

	JitObject(GalaxyJitPtr p)
	{//p is new reference
		m_p = p;
	}
	JitObject(int v)
	{
		m_p = g_pHost->from_int(v);
	}
	JitObject(long long v)
	{
		m_p = g_pHost->from_longlong(v);
	}
	JitObject(float v)
	{
		m_p = g_pHost->from_float(v);
	}
	JitObject(const char* v)
	{
		m_p = g_pHost->from_str(v);
	}
	JitObject(const std::string& v)
	{
		m_p = g_pHost->from_str(v.c_str());
	}
	JitObject(const JitObject& self)
	{
		m_p = self.m_p;
		if (m_p)
		{
			g_pHost->AddRef(m_p);
		}
	}
	JitObject& operator=(const JitObject& o)
	{
		if (m_p)
		{
			g_pHost->Release(m_p);
		}
		m_p = o.m_p;
		if (m_p)
		{
			g_pHost->AddRef(m_p);
		}
		return *this;
	}
	~JitObject()
	{
		if (m_p)
		{
			g_pHost->Release(m_p);
		}
	}
	inline operator GalaxyJitPtr () const
	{
		if (m_p)
		{
			g_pHost->AddRef(m_p);
		}
		return m_p;
	}
	inline JitObjectRef<JitObject> operator[](int i)
	{
		return JitObjectRef<JitObject>(m_p, i);
	}

	inline JitObjectRef<JitObject> operator[](const char* key)
	{
		return JitObjectRef<JitObject>(m_p,key);
	}
	inline bool ContainKey(const char* key)
	{
		return g_pHost->ContainKey(m_p, JitObject(key));
	}
	int GetCount()
	{
		return g_pHost->GetCount(m_p);
	}
	operator int() const 
	{ 
		return g_pHost->to_int(m_p);
	}
	operator long long() const
	{
		return g_pHost->to_longlong(m_p);
	}
	operator float() const
	{
		return g_pHost->to_float(m_p);
	}
	explicit operator std::string() const
	{
		auto sz =  g_pHost->to_str(m_p);
		std::string str(sz);
		g_pHost->Free(sz);
		return str;
	}
	inline JitObject Call(int size, GalaxyJitPtr* ptrs)
	{
		GalaxyJitPtr retPtr = g_pHost->Call(m_p, size, ptrs);
		delete[] ptrs;
		return retPtr;
	}
	inline JitObject Call(int size, GalaxyJitPtr* ptrs, GalaxyJitPtr kwargs)
	{
		GalaxyJitPtr retPtr = g_pHost->Call(m_p, size, ptrs, kwargs);
		delete[] ptrs;
		return retPtr;
	}
	template<typename... VarList>
	JitObject operator()(VarList... args)
	{
		GalaxyJitPtr* ptrs = nullptr;
		const int size = sizeof...(args);
		JitObject objs[size] = { args... };
		ptrs = new GalaxyJitPtr[size];
		for (int i = 0; i < size; i++)
		{
			ptrs[i] = objs[i].m_p;
		}
		return Call(size,ptrs);
	}
	JitObject operator()()
	{
		return Call(0, nullptr);
	}
protected:
	GalaxyJitPtr m_p = nullptr;
};
#if 0
JitObject operator+(const JitObject& v1, const JitObject& v2)
{
	JitObject o;
	return o;
}
#endif
class JitBorrowObject :
	public JitObject
{
public:
	JitBorrowObject() 
		:JitObject()
	{

	}
	JitBorrowObject(GalaxyJitPtr p) 
		:JitObject()
	{
		if (p)
		{//if p is borrowed, means caller doesn't increase the refcount
		//so we increase here 
			g_pHost->AddRef(p);
		}
		m_p = p;
	}
};
template<typename ItemData_Type>
class JitArray:
	public JitObject
{
public:
	JitArray() 
		:JitObject()
	{

	}
	JitArray(const JitObject& obj)
		:JitObject(obj)
	{
		m_data = (ItemData_Type*)g_pHost->GetDataPtr(m_p);
		int itemType = 0;
		g_pHost->GetDataDesc(m_p, itemType,
			m_dims, m_strides);
		m_itemdatatype = (JIT_DATA_TYPES)itemType;
		int a = 1;
		m_dimProd.push_back(a);
		for (int i = m_dims.size() - 1; i >= 1; i--)
		{
			a *= (int)m_dims[i];
			m_dimProd.insert(m_dimProd.begin(), a);
		}
	}
	JitArray(int nd, unsigned long long* dims)
	{
		for (int i = 0; i < nd; i++)
		{
			m_dims.push_back(dims[i]);
		}
		int a = 1;
		m_dimProd.push_back(a);
		for (int i = nd - 1; i >= 1; i--)
		{
			a *= (int)dims[i];
			m_dimProd.insert(m_dimProd.begin(), a);
		}
		SetItemType();
		m_p = g_pHost->NewArray(nd, dims, (int)m_itemdatatype);
		m_data = (ItemData_Type*)g_pHost->GetDataPtr(m_p);
	}

	template<typename... index>
	inline ItemData_Type& operator()(index... i)
	{
		const int size = sizeof...(i);
		long long idx[size] = { i... };

		int addr = idx[0] * m_dimProd[0];
		for (int i = 1; i < m_dimProd.size(); i++)
		{
			addr += idx[i] * m_dimProd[i];
		}
		return m_data[addr];
	}
	ItemData_Type* GetData()
	{
		return m_data;
	}
	std::vector<unsigned long long>& GetDims()
	{
		return m_dims;
	}
protected:
	void SetItemType();
	std::vector<int> m_dimProd;
	JIT_DATA_TYPES m_itemdatatype;
	std::vector<unsigned long long> m_dims;
	std::vector<unsigned long long> m_strides;
	ItemData_Type* m_data;
};

template<>
inline void JitArray<float>::SetItemType()
{
	m_itemdatatype = JIT_DATA_TYPES::FLOAT;
}

template<>
inline void JitArray<int>::SetItemType()
{
	m_itemdatatype = JIT_DATA_TYPES::INT;
}

#endif //_JIT_OBJECT_H_
