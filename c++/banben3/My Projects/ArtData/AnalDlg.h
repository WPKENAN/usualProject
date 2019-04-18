#if !defined(AFX_ANALDLG_H__80BD0F99_1685_4293_9B6F_3C747C8B2084__INCLUDED_)
#define AFX_ANALDLG_H__80BD0F99_1685_4293_9B6F_3C747C8B2084__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000
// AnalDlg.h : header file
//

/////////////////////////////////////////////////////////////////////////////
// CAnalDlg dialog

class CAnalDlg : public CDialog
{
// Construction
public:
	CAnalDlg(CWnd* pParent = NULL);   // standard constructor

// Dialog Data
	//{{AFX_DATA(CAnalDlg)
	enum { IDD = IDD_DIALOG1 };
	//}}AFX_DATA


// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CAnalDlg)
	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support
	//}}AFX_VIRTUAL

// Implementation
protected:

	// Generated message map functions
	//{{AFX_MSG(CAnalDlg)
		// NOTE: the ClassWizard will add member functions here
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_ANALDLG_H__80BD0F99_1685_4293_9B6F_3C747C8B2084__INCLUDED_)
