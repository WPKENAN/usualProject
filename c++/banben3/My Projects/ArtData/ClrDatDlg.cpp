#include "stdafx.h"
#include "ArtData.h"
#include "ClrDatDlg.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#undef THIS_FILE
static char THIS_FILE[] = __FILE__;
#endif
// ClrDatDlg.cpp : implementation file
//


/////////////////////////////////////////////////////////////////////////////
// CClrDatDlg dialog


CClrDatDlg::CClrDatDlg(CWnd* pParent /*=NULL*/)
	: CDialog(CClrDatDlg::IDD, pParent)
{
	//{{AFX_DATA_INIT(CClrDatDlg)
		// NOTE: the ClassWizard will add member initialization here
	//}}AFX_DATA_INIT
}


void CClrDatDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
	//{{AFX_DATA_MAP(CClrDatDlg)
		// NOTE: the ClassWizard will add DDX and DDV calls here
	//}}AFX_DATA_MAP
}


BEGIN_MESSAGE_MAP(CClrDatDlg, CDialog)
	//{{AFX_MSG_MAP(CClrDatDlg)
		// NOTE: the ClassWizard will add message map macros here
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CClrDatDlg message handlers
