#if !defined(AFX_ANAL2_H__9758A6AD_CF0D_42EB_ABB8_9F3B0397086A__INCLUDED_)
#define AFX_ANAL2_H__9758A6AD_CF0D_42EB_ABB8_9F3B0397086A__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000
// ANAL2.h : header file
//

/////////////////////////////////////////////////////////////////////////////
// CANAL2 dialog

class CANAL2 : public CDialog
{
// Construction
public:
	CANAL2(CWnd* pParent = NULL);   // standard constructor

// Dialog Data
	//{{AFX_DATA(CANAL2)
	enum { IDD = IDD_ANALYSIS2 };
		// NOTE: the ClassWizard will add data members here
	//}}AFX_DATA


// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CANAL2)
	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support
	//}}AFX_VIRTUAL

// Implementation
protected:

	// Generated message map functions
	//{{AFX_MSG(CANAL2)
		// NOTE: the ClassWizard will add member functions here
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_ANAL2_H__9758A6AD_CF0D_42EB_ABB8_9F3B0397086A__INCLUDED_)
