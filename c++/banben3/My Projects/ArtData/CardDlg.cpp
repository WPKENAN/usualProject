#include "stdafx.h"
#include "ArtData.h"
#include "CardDlg.h"
#include "MainFrm.h"
#include "ArtDataView.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#undef THIS_FILE
static char THIS_FILE[] = __FILE__;
#endif
// CardDlg.cpp : implementation file
//


/////////////////////////////////////////////////////////////////////////////
// CCardDlg dialog


CCardDlg::CCardDlg(CWnd* pParent /*=NULL*/)
	: CDialog(CCardDlg::IDD, pParent)
{
	//{{AFX_DATA_INIT(CCardDlg)
	m_iSmplTime = 0;
	//}}AFX_DATA_INIT
	temp=0;
	m_bCdDlgShown=FALSE;
}


void CCardDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
	//{{AFX_DATA_MAP(CCardDlg)
	DDX_Control(pDX, IDC_SMPL_TIME, m_cSmplTime);
	DDX_Control(pDX, IDC_SMPL_FRQ, m_cSmplFrq);
	DDX_Control(pDX, IDC_SIGNL_GRND, m_cSignlGrnd);
	DDX_Control(pDX, IDC_SIGNL_RNG, m_cSignlRng);
	DDX_Control(pDX, IDC_SIGNL_GAIN, m_cSignlGain);
	DDX_Control(pDX, IDC_LST_CHNNL, m_cLastChnnl);
	DDX_Control(pDX, IDC_FST_CHNNL, m_cFirstChnnl);
	DDX_Text(pDX, IDC_SMPL_TIME, m_iSmplTime);
	DDV_MinMaxUInt(pDX, m_iSmplTime, 0, 7200);
	//}}AFX_DATA_MAP
}


BEGIN_MESSAGE_MAP(CCardDlg, CDialog)
	//{{AFX_MSG_MAP(CCardDlg)
	ON_CBN_SELCHANGE(IDC_FST_CHNNL, OnSelchangeFstChnnl)
	ON_CBN_SELCHANGE(IDC_SIGNL_GRND, OnSelchangeSignlGrnd)
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CCardDlg message handlers

//DEL BOOL CCardDlg::OnInitDialog() 
//DEL {
//DEL 	CDialog::OnInitDialog();
//DEL 	
//DEL 	// TODO: Add extra initialization here
//DEL 	((CComboBox*)GetDlgItem(IDC_SIGNL_GAIN))->SetCurSel(0);
//DEL 	((CComboBox*)GetDlgItem(IDC_SIGNL_GRND))->SetCurSel(0);
//DEL 	((CComboBox*)GetDlgItem(IDC_SIGNL_RNG))->SetCurSel(0);
//DEL 	((CComboBox*)GetDlgItem(IDC_FST_CHNNL))->SetCurSel(0);
//DEL 	((CComboBox*)GetDlgItem(IDC_LST_CHNNL))->SetCurSel(0);
//DEL 	((CComboBox*)GetDlgItem(IDC_SMPL_FRQ))->SetCurSel(0);
//DEL 
//DEL 	return TRUE;  // return TRUE unless you set the focus to a control
//DEL 	              // EXCEPTION: OCX Property Pages should return FALSE
//DEL }

void CCardDlg::OnSelchangeFstChnnl() 
{
	// TODO: Add your control notification handler code here
		int fChnnl,lChnnl,finc;
	CString str;
 
	CMainFrame *pMain = (CMainFrame *)AfxGetApp()->m_pMainWnd;
	CArtDataView *pView = (CArtDataView *)pMain->GetActiveView();

	fChnnl=((CComboBox*)GetDlgItem(IDC_FST_CHNNL))->GetCurSel();
	lChnnl=((CComboBox*)GetDlgItem(IDC_LST_CHNNL))->GetCurSel();
	((CComboBox*)GetDlgItem(IDC_LST_CHNNL))->ResetContent();
	for(int i=fChnnl;i<pView->m_iChAmount[m_cSignlGrnd.GetCurSel()];i++)
 	{
		str.Empty();
		str.Format("%d",i);	
		((CComboBox*)GetDlgItem(IDC_LST_CHNNL))->AddString(str);
 	}

	finc=fChnnl-temp;
	temp=fChnnl;
	if(finc<=lChnnl)
	{
		((CComboBox*)GetDlgItem(IDC_LST_CHNNL))->SetCurSel(lChnnl-finc);
	}
	else
	{
		((CComboBox*)GetDlgItem(IDC_LST_CHNNL))->SetCurSel(0);
	}
}

//DEL void CCardDlg::OnOK() 
//DEL {
//DEL 	CDialog::OnOK();
//DEL }

//DEL void CCardDlg::OnSmplParm() 
//DEL {
//DEL 	// TODO: Add your command handler code here
//DEL }

//DEL void CCardDlg::OnOK() 
//DEL {
//DEL 	// TODO: Add extra validation here
//DEL 	CDialog::OnOK();
//DEL }

void CCardDlg::OnOK() 
{
	// TODO: Add extra validation here
	CMainFrame *pMain = (CMainFrame *)AfxGetApp()->m_pMainWnd;
	CArtDataView *pView = (CArtDataView *)pMain->GetActiveView();

	pView->m_sCdParm.FirstChannel=m_cFirstChnnl.GetCurSel();
	pView->m_sCdParm.Gains=m_cSignlGain.GetCurSel();
	pView->m_sCdParm.GroundingMode=m_cSignlGrnd.GetCurSel();
	pView->m_sCdParm.InputRange=m_cSignlRng.GetCurSel();
	pView->m_sCdParm.LastChannel=m_cLastChnnl.GetCurSel();
	pView->m_iSmplFrq=m_cSmplFrq.GetCurSel();
	pView->m_iSmplTime=GetDlgItemInt(IDC_SMPL_TIME);

	m_bCdDlgShown=FALSE;

	DestroyWindow();//	CDialog::OnOK();

}

void CCardDlg::OnSelchangeSignlGrnd() 
{
	// TODO: Add your control notification handler code here
	CMainFrame *pMain = (CMainFrame *)AfxGetApp()->m_pMainWnd;
	CArtDataView *pView = (CArtDataView *)pMain->GetActiveView();
		
	((CComboBox*)GetDlgItem(IDC_FST_CHNNL))->ResetContent();
	((CComboBox*)GetDlgItem(IDC_LST_CHNNL))->ResetContent();
	CString str;
	for(int i=0;i<pView->m_iChAmount[m_cSignlGrnd.GetCurSel()];i++)
 	{
		str.Empty();
		str.Format("%d",i);	
		((CComboBox*)GetDlgItem(IDC_FST_CHNNL))->AddString(str);
		((CComboBox*)GetDlgItem(IDC_LST_CHNNL))->AddString(str);
 	}
	((CComboBox*)GetDlgItem(IDC_FST_CHNNL))->SetCurSel(0);
	((CComboBox*)GetDlgItem(IDC_LST_CHNNL))->SetCurSel(0);
}

void CCardDlg::OnCancel() 
{
	// TODO: Add extra cleanup here
	m_bCdDlgShown=FALSE;

	DestroyWindow();
//	CDialog::OnCancel();
}
