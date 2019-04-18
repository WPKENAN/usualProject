// MainFrm.h : interface of the CMainFrame class
//
/////////////////////////////////////////////////////////////////////////////

#if !defined(AFX_MAINFRM_H__8966A01B_979F_4906_BE9B_25AB51C92D1D__INCLUDED_)
#define AFX_MAINFRM_H__8966A01B_979F_4906_BE9B_25AB51C92D1D__INCLUDED_

#include "AnalDlg.h"	// Added by ClassView
#include "AnalDlg2.h"	// Added by ClassView
#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000
#include <vector>
using namespace std;

class CMainFrame : public CFrameWnd
{
	
protected: // create from serialization only
	CMainFrame();
	DECLARE_DYNCREATE(CMainFrame)

// Attributes
public:
//	vector<CString> m_strPromptTxtVct;
//	vector<int> m_iTxtDistncVct;
// Operations
public:

// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CMainFrame)
	virtual BOOL PreCreateWindow(CREATESTRUCT& cs);
	//}}AFX_VIRTUAL

// Implementation
public:
//	CFileDialog m_hFileDlg;
	CAnalDlg  m_cAnalDlg;
	CAnalDlg2 m_cAnalDlg2;
	virtual ~CMainFrame();
#ifdef _DEBUG
	virtual void AssertValid() const;
	virtual void Dump(CDumpContext& dc) const;
#endif

protected:  // control bar embedded members
	CStatusBar  m_wndStatusBar;
	CToolBar    m_wndToolBar;

// Generated message map functions
protected:
	//{{AFX_MSG(CMainFrame)
	afx_msg int OnCreate(LPCREATESTRUCT lpCreateStruct);
	afx_msg void OnUpdateFileNew(CCmdUI* pCmdUI);
	afx_msg void OnUpdateFileOpen(CCmdUI* pCmdUI);
	afx_msg void OnUpdateFileSave(CCmdUI* pCmdUI);
	afx_msg void OnUpdateFileSaveAs(CCmdUI* pCmdUI);
	afx_msg void OnAnalsysGen();
	afx_msg void OnUpdateSmplReset(CCmdUI* pCmdUI);
	afx_msg void OnUpdateClear(CCmdUI* pCmdUI);
	afx_msg void OnUpdateSmplStart(CCmdUI* pCmdUI);
	afx_msg void OnUpdateAnalsysGen(CCmdUI* pCmdUI);
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};

/////////////////////////////////////////////////////////////////////////////

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_MAINFRM_H__8966A01B_979F_4906_BE9B_25AB51C92D1D__INCLUDED_)
