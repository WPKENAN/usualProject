#if !defined(AFX_CLRDATDLG_H__AB141F48_6D26_4557_809A_2E56B27BBAE9__INCLUDED_)
#define AFX_CLRDATDLG_H__AB141F48_6D26_4557_809A_2E56B27BBAE9__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000
// ClrDatDlg.h : header file
//

/////////////////////////////////////////////////////////////////////////////
// CClrDatDlg dialog

class CClrDatDlg : public CDialog
{
// Construction
public:
	CClrDatDlg(CWnd* pParent = NULL);   // standard constructor

// Dialog Data
	//{{AFX_DATA(CClrDatDlg)
	enum { IDD = IDD_CLRDAT };
		// NOTE: the ClassWizard will add data members here
	//}}AFX_DATA


// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CClrDatDlg)
	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support
	//}}AFX_VIRTUAL

// Implementation
protected:

	// Generated message map functions
	//{{AFX_MSG(CClrDatDlg)
		// NOTE: the ClassWizard will add member functions here
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_CLRDATDLG_H__AB141F48_6D26_4557_809A_2E56B27BBAE9__INCLUDED_)
