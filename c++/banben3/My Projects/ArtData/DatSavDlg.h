#if !defined(AFX_DATSAVDLG_H__06CA5432_929D_4AA1_BE00_16BA17794082__INCLUDED_)
#define AFX_DATSAVDLG_H__06CA5432_929D_4AA1_BE00_16BA17794082__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000
// DatSavDlg.h : header file
//

/////////////////////////////////////////////////////////////////////////////
// CDatSavDlg dialog

class CDatSavDlg : public CDialog
{
// Construction
public:
	CDatSavDlg(CWnd* pParent = NULL);   // standard constructor

// Dialog Data
	//{{AFX_DATA(CDatSavDlg)
	enum { IDD = IDD_DATA_SAVE };
		// NOTE: the ClassWizard will add data members here
	//}}AFX_DATA


// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CDatSavDlg)
	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support
	//}}AFX_VIRTUAL

// Implementation
protected:

	// Generated message map functions
	//{{AFX_MSG(CDatSavDlg)
		// NOTE: the ClassWizard will add member functions here
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_DATSAVDLG_H__06CA5432_929D_4AA1_BE00_16BA17794082__INCLUDED_)
