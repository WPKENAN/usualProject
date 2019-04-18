#if !defined(AFX_CARDDLG_H__49F54D1A_F148_4BB9_A94F_8DFD5AB48BFE__INCLUDED_)
#define AFX_CARDDLG_H__49F54D1A_F148_4BB9_A94F_8DFD5AB48BFE__INCLUDED_

#include "Usb5935.h" //#include "C:\ART\USB5935\Samples\VC\Simple\AD\Usb5935.h"	// Added by ClassView
#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000
// CardDlg.h : header file
//

/////////////////////////////////////////////////////////////////////////////
// CCardDlg dialog

class CCardDlg : public CDialog
{
// Construction
public:
	BOOL m_bCdDlgShown;

//	USB5935_PARA_AD m_sCdParm;
	CCardDlg(CWnd* pParent = NULL);   // standard constructor

// Dialog Data
	//{{AFX_DATA(CCardDlg)
	enum { IDD = IDD_CARDDLG };
	CEdit	m_cSmplTime;
	CComboBox	m_cSmplFrq;
	CComboBox	m_cSignlGrnd;
	CComboBox	m_cSignlRng;
	CComboBox	m_cSignlGain;
	CComboBox	m_cLastChnnl;
	CComboBox	m_cFirstChnnl;
	UINT	m_iSmplTime;
	//}}AFX_DATA


// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CCardDlg)
	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support
	//}}AFX_VIRTUAL

// Implementation
protected:

	// Generated message map functions
	//{{AFX_MSG(CCardDlg)
	afx_msg void OnSelchangeFstChnnl();
	virtual void OnOK();
	afx_msg void OnSelchangeSignlGrnd();
	virtual void OnCancel();
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
private:
	int temp;
};

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_CARDDLG_H__49F54D1A_F148_4BB9_A94F_8DFD5AB48BFE__INCLUDED_)
