// ArtDataDoc.h : interface of the CArtDataDoc class
//
/////////////////////////////////////////////////////////////////////////////

#if !defined(AFX_ARTDATADOC_H__3FD50813_E2FB_41AD_9DD2_5282E6A2E35B__INCLUDED_)
#define AFX_ARTDATADOC_H__3FD50813_E2FB_41AD_9DD2_5282E6A2E35B__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000
#include <vector>
using namespace std;

#include <afxtempl.h>


class CArtDataDoc : public CDocument
{
protected: // create from serialization only
	CArtDataDoc();
	DECLARE_DYNCREATE(CArtDataDoc)

// Attributes
public:
//	CString m_s;
//	vector< DWORD > m_dwSmplTime;
	BOOL m_bSaved;          //m_bSaveAsTXT,
	BOOL m_bFromFile;
	vector< vector<float> > m_fDatVct;//y用于保存各通道采集到底数据的二维向量,m_fDatVctb
	vector<long>  m_iCtlVct;//用于记录各通道的各个数据段信息的二维向量vector<>
	long m_iDatPtr;     //通道数据指针
	long m_iAnalCtl[4];  //分析结果控制向量：分析类型，分析的数据通道号

	// Operations
public:

// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CArtDataDoc)
	public:
	virtual BOOL OnNewDocument();
	virtual void Serialize(CArchive& ar);
	//}}AFX_VIRTUAL

// Implementation
public:
	virtual ~CArtDataDoc();
#ifdef _DEBUG
	virtual void AssertValid() const;
	virtual void Dump(CDumpContext& dc) const;
#endif

protected:

// Generated message map functions
protected:
	//{{AFX_MSG(CArtDataDoc)
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};

/////////////////////////////////////////////////////////////////////////////

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_ARTDATADOC_H__3FD50813_E2FB_41AD_9DD2_5282E6A2E35B__INCLUDED_)
