#if !defined(AFX_ANALDLG2_H__B577AEB2_35C8_4802_9748_8206604EE6DE__INCLUDED_)
#define AFX_ANALDLG2_H__B577AEB2_35C8_4802_9748_8206604EE6DE__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000
// AnalDlg2.h : header file
//

/////////////////////////////////////////////////////////////////////////////
// CAnalDlg2 dialog

class CAnalDlg2 : public CDialog
{
// Construction
public:
	void GetCbBoxSel();
	int m_iAnalType;
	CAnalDlg2(CWnd* pParent = NULL);   // standard constructor

// Dialog Data
	//{{AFX_DATA(CAnalDlg2)
	enum { IDD = IDD_ANALYSIS2 };
	CComboBox	m_cAnalType;
	int		m_iDataSeg;
	int		m_iDataSeg2;
	//}}AFX_DATA


// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CAnalDlg2)
	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support
	//}}AFX_VIRTUAL

// Implementation
protected:

	// Generated message map functions
	//{{AFX_MSG(CAnalDlg2)
	afx_msg void OnShowWindow(BOOL bShow, UINT nStatus);
	afx_msg void OnSelchangeAnaltype();
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_ANALDLG2_H__B577AEB2_35C8_4802_9748_8206604EE6DE__INCLUDED_)
