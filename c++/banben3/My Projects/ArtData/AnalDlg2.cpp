#include "stdafx.h"
#include "ArtData.h"
#include "AnalDlg2.h"
// AnalDlg2.cpp : implementation file
//
#ifdef _DEBUG
#define new DEBUG_NEW
#undef THIS_FILE
static char THIS_FILE[] = __FILE__;
#endif

/////////////////////////////////////////////////////////////////////////////
// CAnalDlg2 dialog


CAnalDlg2::CAnalDlg2(CWnd* pParent /*=NULL*/)
	: CDialog(CAnalDlg2::IDD, pParent)
{
	//{{AFX_DATA_INIT(CAnalDlg2)
	m_iDataSeg = 0;
	m_iDataSeg2 = 0;
	//}}AFX_DATA_INIT
}


void CAnalDlg2::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
	//{{AFX_DATA_MAP(CAnalDlg2)
	DDX_Control(pDX, IDC_ANALTYPE, m_cAnalType);
	DDX_Text(pDX, IDC_DATASEG, m_iDataSeg);
	DDV_MinMaxInt(pDX, m_iDataSeg, 0, 15);
	DDX_Text(pDX, IDC_DATASEG2, m_iDataSeg2);
	DDV_MinMaxInt(pDX, m_iDataSeg2, 0, 15);
	//}}AFX_DATA_MAP
}


BEGIN_MESSAGE_MAP(CAnalDlg2, CDialog)
	//{{AFX_MSG_MAP(CAnalDlg2)
	ON_WM_SHOWWINDOW()
	ON_CBN_SELCHANGE(IDC_ANALTYPE, OnSelchangeAnaltype)
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CAnalDlg2 message handlers

void CAnalDlg2::OnShowWindow(BOOL bShow, UINT nStatus) 
{
	CDialog::OnShowWindow(bShow, nStatus);
	
	// TODO: Add your message handler code here
	m_iAnalType=0;
	m_cAnalType.SetCurSel(m_iAnalType);	
}

void CAnalDlg2::OnSelchangeAnaltype() 
{
	// TODO: Add your control notification handler code here
	m_iAnalType=m_cAnalType.GetCurSel();
	switch(m_iAnalType)
	{
	case 0:
		GetDlgItem(IDC_DATASEG2)->EnableWindow(TRUE);
		break;
	case 1:
		GetDlgItem(IDC_DATASEG2)->EnableWindow(TRUE);
		break;
	case 2:
		GetDlgItem(IDC_DATASEG2)->EnableWindow(TRUE);
		break;
	case 3:
		GetDlgItem(IDC_DATASEG2)->EnableWindow(TRUE);
		break;
	case 4:
		GetDlgItem(IDC_DATASEG2)->EnableWindow(FALSE);
		break;
	case 5:
		GetDlgItem(IDC_DATASEG2)->EnableWindow(FALSE);
		break;
	case 6:
		GetDlgItem(IDC_DATASEG2)->EnableWindow(FALSE);
		break;
	case 7:
		GetDlgItem(IDC_DATASEG2)->EnableWindow(FALSE);
		break;
	case 8:
		GetDlgItem(IDC_DATASEG2)->EnableWindow(FALSE);
		break;
	case 9:
		GetDlgItem(IDC_DATASEG2)->EnableWindow(FALSE);
		break;
	case 10:
		GetDlgItem(IDC_DATASEG2)->EnableWindow(FALSE);
		break;
	}
	
}

void CAnalDlg2::GetCbBoxSel()
{

}
