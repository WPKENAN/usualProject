#include "stdafx.h"
#include "ArtData.h"
#include "AnalDlg.h"
// AnalDlg.cpp : implementation file
//

#ifdef _DEBUG
#define new DEBUG_NEW
#undef THIS_FILE
static char THIS_FILE[] = __FILE__;
#endif

/////////////////////////////////////////////////////////////////////////////
// CAnalDlg dialog


CAnalDlg::CAnalDlg(CWnd* pParent /*=NULL*/)
	: CDialog(CAnalDlg::IDD, pParent)
{
	//{{AFX_DATA_INIT(CAnalDlg)
	//}}AFX_DATA_INIT
}


void CAnalDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
	//{{AFX_DATA_MAP(CAnalDlg)
	//}}AFX_DATA_MAP
}


BEGIN_MESSAGE_MAP(CAnalDlg, CDialog)
	//{{AFX_MSG_MAP(CAnalDlg)
		// NOTE: the ClassWizard will add message map macros here
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CAnalDlg message handlers

