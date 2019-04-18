// ANAL2.cpp : implementation file
//

#include "stdafx.h"
#include "ArtData.h"
#include "ANAL2.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#undef THIS_FILE
static char THIS_FILE[] = __FILE__;
#endif

/////////////////////////////////////////////////////////////////////////////
// CANAL2 dialog


CANAL2::CANAL2(CWnd* pParent /*=NULL*/)
	: CDialog(CANAL2::IDD, pParent)
{
	//{{AFX_DATA_INIT(CANAL2)
		// NOTE: the ClassWizard will add member initialization here
	//}}AFX_DATA_INIT
}


void CANAL2::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
	//{{AFX_DATA_MAP(CANAL2)
		// NOTE: the ClassWizard will add DDX and DDV calls here
	//}}AFX_DATA_MAP
}


BEGIN_MESSAGE_MAP(CANAL2, CDialog)
	//{{AFX_MSG_MAP(CANAL2)
		// NOTE: the ClassWizard will add message map macros here
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CANAL2 message handlers
