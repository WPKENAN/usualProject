#include "stdafx.h"
#include "ArtData.h"
#include "DatSavDlg.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#undef THIS_FILE
static char THIS_FILE[] = __FILE__;
#endif
// DatSavDlg.cpp : implementation file
//


/////////////////////////////////////////////////////////////////////////////
// CDatSavDlg dialog


CDatSavDlg::CDatSavDlg(CWnd* pParent /*=NULL*/)
	: CDialog(CDatSavDlg::IDD, pParent)
{
	//{{AFX_DATA_INIT(CDatSavDlg)
		// NOTE: the ClassWizard will add member initialization here
	//}}AFX_DATA_INIT
}


void CDatSavDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
	//{{AFX_DATA_MAP(CDatSavDlg)
		// NOTE: the ClassWizard will add DDX and DDV calls here
	//}}AFX_DATA_MAP
}


BEGIN_MESSAGE_MAP(CDatSavDlg, CDialog)
	//{{AFX_MSG_MAP(CDatSavDlg)
		// NOTE: the ClassWizard will add message map macros here
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CDatSavDlg message handlers
