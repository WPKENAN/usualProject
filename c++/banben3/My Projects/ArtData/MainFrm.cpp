#include "stdafx.h"
#include "ArtData.h"
#include "SigAnals.h"
#include "MainFrm.h"
#include "ArtDataView.h"
#include "stdlib.h"
#include "matlib.h"
// MainFrm.cpp : implementation of the CMainFrame class
//


#define isBadHandle(h) ( (h) == NULL || (h) == INVALID_HANDLE_VALUE )

#ifdef _DEBUG
#define new DEBUG_NEW
#undef THIS_FILE
static char THIS_FILE[] = __FILE__;
#endif

/////////////////////////////////////////////////////////////////////////////
// CMainFrame

IMPLEMENT_DYNCREATE(CMainFrame, CFrameWnd)

BEGIN_MESSAGE_MAP(CMainFrame, CFrameWnd)
	//{{AFX_MSG_MAP(CMainFrame)
	ON_WM_CREATE()
	ON_UPDATE_COMMAND_UI(ID_FILE_NEW, OnUpdateFileNew)
	ON_UPDATE_COMMAND_UI(ID_FILE_OPEN, OnUpdateFileOpen)
	ON_UPDATE_COMMAND_UI(ID_FILE_SAVE, OnUpdateFileSave)
	ON_UPDATE_COMMAND_UI(ID_FILE_SAVE_AS, OnUpdateFileSaveAs)
	ON_COMMAND(IDM_ANALSYS_GEN, OnAnalsysGen)
	ON_UPDATE_COMMAND_UI(IDM_SMPL_RESET, OnUpdateSmplReset)
	ON_UPDATE_COMMAND_UI(IDM_CLEAR, OnUpdateClear)
	ON_UPDATE_COMMAND_UI(IDM_SMPL_START, OnUpdateSmplStart)
	ON_UPDATE_COMMAND_UI(IDM_ANALSYS_GEN, OnUpdateAnalsysGen)
	//}}AFX_MSG_MAP
	// Global help commands
	ON_COMMAND(ID_HELP_FINDER, CFrameWnd::OnHelpFinder)
	ON_COMMAND(ID_HELP, CFrameWnd::OnHelp)
	ON_COMMAND(ID_CONTEXT_HELP, CFrameWnd::OnContextHelp)
	ON_COMMAND(ID_DEFAULT_HELP, CFrameWnd::OnHelpFinder)
END_MESSAGE_MAP()

static UINT indicators[] =
{
	ID_SEPARATOR,           // status line indicator
	ID_INDICATOR_CAPS,
	ID_INDICATOR_NUM,
	ID_INDICATOR_SCRL,
};

/////////////////////////////////////////////////////////////////////////////
// CMainFrame construction/destruction

CMainFrame::CMainFrame()
{
	// TODO: add member initialization code here
//	m_bAutoMenuEnable=FALSE;
}

CMainFrame::~CMainFrame()
{
	     HANDLE hProcess;
         hProcess = OpenProcess( PROCESS_TERMINATE, true, GetCurrentProcessId() );
         if ( isBadHandle( hProcess ) ){}
             //ShowMessage( "OpenProcess() failed, err = %lu\n");
         else {
             // kill process
             TerminateProcess( hProcess, (DWORD) -1 );
         }
         // close handle
         CloseHandle( hProcess );

}

int CMainFrame::OnCreate(LPCREATESTRUCT lpCreateStruct)
{
	HICON m_hIcon;
	m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);//IDI_ICON1
	SetIcon(m_hIcon, TRUE); // Set big icon
	SetIcon(m_hIcon, FALSE); // Set small icon
	if (CFrameWnd::OnCreate(lpCreateStruct) == -1)
		return -1;
	
	if (!m_wndToolBar.CreateEx(this, TBSTYLE_FLAT, WS_CHILD | WS_VISIBLE | CBRS_TOP
		| CBRS_GRIPPER | CBRS_TOOLTIPS | CBRS_FLYBY | CBRS_SIZE_DYNAMIC) ||
		!m_wndToolBar.LoadToolBar(IDR_TOOLBAR1))//IDR_MAINFRAME))
	{
		TRACE0("Failed to create toolbar\n");
		return -1;      // fail to create
	}

	if (!m_wndStatusBar.Create(this) ||
		!m_wndStatusBar.SetIndicators(indicators,
		  sizeof(indicators)/sizeof(UINT)))
	{
		TRACE0("Failed to create status bar\n");
		return -1;      // fail to create
	}

	// TODO: Delete these three lines if you don't want the toolbar to
	//  be dockable
	m_wndToolBar.EnableDocking(CBRS_ALIGN_ANY);
	EnableDocking(CBRS_ALIGN_ANY);
	DockControlBar(&m_wndToolBar);
/*
	GetMenu()->GetSubMenu(0)->EnableMenuItem(ID_FILE_SAVE,MF_BYCOMMAND|MF_DISABLED|MF_GRAYED);
	GetMenu()->GetSubMenu(0)->EnableMenuItem(ID_FILE_SAVE_AS,MF_BYCOMMAND|MF_DISABLED|MF_GRAYED);
	GetMenu()->GetSubMenu(1)->EnableMenuItem(IDM_SMPL_STOP,MF_BYCOMMAND|MF_DISABLED|MF_GRAYED);
	GetMenu()->GetSubMenu(2)->EnableMenuItem(0,MF_BYPOSITION|MF_DISABLED|MF_GRAYED);
	GetMenu()->GetSubMenu(2)->EnableMenuItem(1,MF_BYPOSITION|MF_DISABLED|MF_GRAYED);

*/	return 0;
}

BOOL CMainFrame::PreCreateWindow(CREATESTRUCT& cs)
{
	if( !CFrameWnd::PreCreateWindow(cs) )
		return FALSE;
	// TODO: Modify the Window class or styles here by modifying
	//  the CREATESTRUCT cs

	return TRUE;
}

/////////////////////////////////////////////////////////////////////////////
// CMainFrame diagnostics

#ifdef _DEBUG
void CMainFrame::AssertValid() const
{
	CFrameWnd::AssertValid();
}

void CMainFrame::Dump(CDumpContext& dc) const
{
	CFrameWnd::Dump(dc);
}

#endif //_DEBUG

/////////////////////////////////////////////////////////////////////////////
// CMainFrame message handlers


//DEL void CMainFrame::OnSmplParm() 
//DEL {
//DEL 	// TODO: Add your command handler code here
//DEL 	
//DEL }

void CMainFrame::OnUpdateFileNew(CCmdUI* pCmdUI) 
{
	// TODO: Add your command update UI handler code here
	CArtDataView* pView=(CArtDataView*)GetActiveView();
	if(pView->m_bADWorking){pCmdUI->Enable(FALSE);}
	
}

void CMainFrame::OnUpdateFileOpen(CCmdUI* pCmdUI) 
{
	// TODO: Add your command update UI handler code here
	CArtDataView* pView=(CArtDataView*)GetActiveView();
	if(pView->m_bADWorking){pCmdUI->Enable(FALSE);
	GetMenu()->GetSubMenu(1)->EnableMenuItem(6,MF_BYPOSITION|MF_DISABLED|MF_GRAYED);}
	
}

void CMainFrame::OnUpdateFileSave(CCmdUI* pCmdUI) 
{
	// TODO: Add your command update UI handler code here
	CArtDataView* pView=(CArtDataView*)GetActiveView();
	if(pView->m_bADWorking){pCmdUI->Enable(FALSE);}
	
}

void CMainFrame::OnUpdateFileSaveAs(CCmdUI* pCmdUI) 
{
	// TODO: Add your command update UI handler code here
	CArtDataView* pView=(CArtDataView*)GetActiveView();
	if(pView->m_bADWorking){pCmdUI->Enable(FALSE);}
	
}


void CMainFrame::OnAnalsysGen()
{
	// TODO: Add your command handler code here
	CArtDataView* pView=(CArtDataView*)GetActiveView();
	CArtDataDoc* pDoc=pView->GetDocument();

	CClientDC dc(pView);//Invalidate();
	CString str;
		int datcount=pDoc->m_iCtlVct[6];  //数据个数		int 
		double fT,tlength=pDoc->m_iCtlVct[7];   //采样时长;
	
	if(pDoc->m_iCtlVct.size()&&datcount)
	{
//		int analtype,Dseg,Dseg2;
		int k=0;
		int d1=0,d2=0;

		initM(MATCOM_VERSION);

		Mm x1,x2,y;
/*		Mm OMG,real,img,nm;

				mset(gcf(),TM("MenuBar"),TM("None"));
				mset(gcf(),TM("MenuAbout"),TM("Off"));				

		Mm plothandle,pos;
		CWnd *pPIC=NULL;
		m_cAnalDlg.Create(IDD_DIALOG1);
		m_cAnalDlg.ShowWindow(SW_SHOW);
		pPIC=(CWnd*)m_cAnalDlg.GetDlgItem(IDC_STATIC);
*/
		if(IDOK==m_cAnalDlg2.DoModal())
		{
			UpdateData();

			pDoc->m_fDatVct[16].clear();
			pDoc->m_fDatVct[17].clear();

			FILE (*pFile);
			pFile=fopen("Results.ans" , "w" );
			if(NULL==pFile){pView->OutText("无法打开文件Results.ans！");}

			switch(m_cAnalDlg2.m_iAnalType)
			{
			case 0:      //卷积分析
				//Dseg2=m_cAnalDlg2.m_iDataSeg2;
				x1=rand(1,datcount);
				x2=rand(1,datcount);

				if((m_cAnalDlg2.m_iDataSeg>=pDoc->m_iCtlVct[0])&&(m_cAnalDlg2.m_iDataSeg<=pDoc->m_iCtlVct[1]))
				{//输入 的通道号在采集参数范围内
					for(k=0;k<datcount;k++)
					{
						x1.r(1,k+1)=pDoc->m_fDatVct[m_cAnalDlg2.m_iDataSeg][k];
					}
					d1=1;
				}
				else 
				{
					str.Format("卷积：在数据段1输入的通道%d无数据！",m_cAnalDlg2.m_iDataSeg);
					pView->OutText(str);
				}

				if(m_cAnalDlg2.m_iDataSeg2>=pDoc->m_iCtlVct[0]&&m_cAnalDlg2.m_iDataSeg2<=pDoc->m_iCtlVct[1])
				{
					for(k=0;k<datcount;k++)
					{
						x2.r(1,k+1)=pDoc->m_fDatVct[m_cAnalDlg2.m_iDataSeg2][k];
					}
					d2=1;
				}
				else {str.Format("卷积：在数据段2输入的通道%d无数据！",m_cAnalDlg2.m_iDataSeg2);pView->OutText(str);}

				if(2==d1+d2)
				{
					y=conv(x1,x2);

					for (k=0;k<y.cols();k++)
					{
						fprintf(pFile,"%.4g,",y.r(1,k+1));
					}


					pDoc->m_iAnalCtl[0]=0;
					pDoc->m_iAnalCtl[1]=m_cAnalDlg2.m_iDataSeg;
					pDoc->m_iAnalCtl[2]=m_cAnalDlg2.m_iDataSeg2;

					pDoc->m_fDatVct[16].clear();
					pDoc->m_fDatVct[16].push_back(0);
					pDoc->m_fDatVct[16].push_back(tlength*(2*datcount-1)/datcount);

					pDoc->m_fDatVct[17].clear();
					for(k=0;k<y.cols();k++)
					{
						pDoc->m_fDatVct[17].push_back(y.r(1,k+1));
					}
				}
				else{pView->OutText("卷积：输入不完整，不能分析！");}

				fclose(pFile);

				break;

			case 1:      //相关分析
				x1=rand(1,datcount);
				x2=rand(1,datcount);

				if(m_cAnalDlg2.m_iDataSeg>=pDoc->m_iCtlVct[0]&&m_cAnalDlg2.m_iDataSeg<=pDoc->m_iCtlVct[1])
				{
					for(k=0;k<datcount;k++)
					{
						x1.r(1,k+1)=pDoc->m_fDatVct[m_cAnalDlg2.m_iDataSeg][k];
					}
					d1=1;
				}
				else {str.Format("相关分析：在数据段1输入的通道%d无数据！",m_cAnalDlg2.m_iDataSeg);pView->OutText(str);}

				if(m_cAnalDlg2.m_iDataSeg2>=pDoc->m_iCtlVct[0]&&m_cAnalDlg2.m_iDataSeg2<=pDoc->m_iCtlVct[1])
				{
					for(k=0;k<datcount;k++)
					{
						x2.r(1,k+1)=pDoc->m_fDatVct[m_cAnalDlg2.m_iDataSeg2][k];
					}
					d2=1;
				}
				else {str.Format("相关分析：在数据段2输入的通道%d无数据！",m_cAnalDlg2.m_iDataSeg);pView->OutText(str);}

				if(2==d1+d2)
				{
					y=corrcoef(x1,x2);

					fprintf(pFile,"通道%d与通道%d的相关系数矩阵：\n%.4g,%.4g\n%.4g,%.4g\n",m_cAnalDlg2.m_iDataSeg,m_cAnalDlg2.m_iDataSeg2,y.r(1,1),y.r(1,2),y.r(2,1),y.r(2,2));
					

					pDoc->m_iAnalCtl[0]=1;
					pDoc->m_iAnalCtl[1]=m_cAnalDlg2.m_iDataSeg;
					pDoc->m_iAnalCtl[2]=m_cAnalDlg2.m_iDataSeg2;
					
					pDoc->m_fDatVct[16].clear();
					pDoc->m_fDatVct[16].push_back(2);
					pDoc->m_fDatVct[16].push_back(2);

					pDoc->m_fDatVct[17].clear();
					for (k=0;k<2;k++)
					{  
						for(int n=0;n<2;n++){pDoc->m_fDatVct[17].push_back(y.r(k+1,n+1));}
					} 

					str.Format("通道%d与%d的相关系数矩阵为：%f,%f;  %f,%f",m_cAnalDlg2.m_iDataSeg,m_cAnalDlg2.m_iDataSeg2,y.r(1,1),y.r(1,2),y.r(2,1),y.r(2,2));
					pView->OutText(str);
				}

				else if(d1||d2){pView->OutText("不用分析都知道自相关系数是 1");}

				fclose(pFile); 

				break;

			case 2:      //协方差分析
				x1=rand(1,datcount);
				x2=rand(1,datcount);

				if(m_cAnalDlg2.m_iDataSeg>=pDoc->m_iCtlVct[0]&&m_cAnalDlg2.m_iDataSeg<=pDoc->m_iCtlVct[1])
				{
					for(k=0;k<datcount;k++)
					{
						x1.r(1,k+1)=pDoc->m_fDatVct[m_cAnalDlg2.m_iDataSeg][k];
					}
					d1=1;
				}
				else {str.Format("协方差：在数据段1输入的通道%d无数据！",m_cAnalDlg2.m_iDataSeg);pView->OutText(str);}

				if(m_cAnalDlg2.m_iDataSeg2>=pDoc->m_iCtlVct[0]&&m_cAnalDlg2.m_iDataSeg2<=pDoc->m_iCtlVct[1])
				{
					for(k=0;k<datcount;k++)
					{
						x2.r(1,k+1)=pDoc->m_fDatVct[m_cAnalDlg2.m_iDataSeg2][k];
					}
					d2=1;
				}
				else 
				{
					str.Format("协方差：在数据段2输入的通道%d无数据！",m_cAnalDlg2.m_iDataSeg2);pView->OutText(str);
				}

				if(d1)	{y=cov(x1); fprintf(pFile,"通道%d的协方差：%.4g,",m_cAnalDlg2.m_iDataSeg,y.r(1,1));				
					
					pDoc->m_iAnalCtl[0]=2;
					pDoc->m_iAnalCtl[1]=m_cAnalDlg2.m_iDataSeg;
					pDoc->m_iAnalCtl[2]=1999908;

					pDoc->m_fDatVct[16].clear();
					pDoc->m_fDatVct[16].push_back(1);
					
					pDoc->m_fDatVct[17].clear();
					pDoc->m_fDatVct[17].push_back(y.r(1,1));

					str.Format("通道%d的协方差为：%f",m_cAnalDlg2.m_iDataSeg,y.r(1,1));
					pView->OutText(str);
					
				}
				else if(d2) {y=cov(x2);	fprintf(pFile,"通道%d的协方差：%.4g,",m_cAnalDlg2.m_iDataSeg2,y.r(1,1));
					
					pDoc->m_iAnalCtl[0]=2;
					pDoc->m_iAnalCtl[1]=m_cAnalDlg2.m_iDataSeg2;
					pDoc->m_iAnalCtl[2]=1999998;

					pDoc->m_fDatVct[16].clear();
					pDoc->m_fDatVct[16].push_back(1);
					
					pDoc->m_fDatVct[17].clear();
					pDoc->m_fDatVct[17].push_back(y.r(1,1));
					
					str.Format("通道%d的协方差为：%f",m_cAnalDlg2.m_iDataSeg2,y.r(1,1));
					pView->OutText(str);
				}
				else if(2==d1+d2){y=cov(x1,x2);
					fprintf(pFile,"通道%d与%d的协方差矩阵：\n%.4g, %.4g  \n%.4g,%.4g\n",m_cAnalDlg2.m_iDataSeg,m_cAnalDlg2.m_iDataSeg2,y.r(1,1),y.r(1,2),y.r(2,1),y.r(2,2));
					
					pDoc->m_iAnalCtl[0]=2;
					pDoc->m_iAnalCtl[1]=m_cAnalDlg2.m_iDataSeg;
					pDoc->m_iAnalCtl[2]=m_cAnalDlg2.m_iDataSeg2;

					pDoc->m_fDatVct[16].clear();
					pDoc->m_fDatVct[16].push_back(1);

					pDoc->m_fDatVct[17].clear();
					pDoc->m_fDatVct[17].push_back(y.r(1,1));
					pDoc->m_fDatVct[17].push_back(y.r(1,2));
					pDoc->m_fDatVct[17].push_back(y.r(2,1));
					pDoc->m_fDatVct[17].push_back(y.r(2,2));

					str.Format("通道%d与%d的协方差矩阵：%f, %f;  %f,%f",m_cAnalDlg2.m_iDataSeg,m_cAnalDlg2.m_iDataSeg2,y.r(1,1),y.r(1,2),y.r(2,1),y.r(2,2));
					
					pView->OutText(str);

				}

			    fclose(pFile); 

				break;

			case 3:      //反卷积分析
				x1=rand(1,datcount);
				x2=rand(1,datcount);

				//for(k=0;k<datcount;k++)
				if(m_cAnalDlg2.m_iDataSeg>=pDoc->m_iCtlVct[0]&&m_cAnalDlg2.m_iDataSeg<=pDoc->m_iCtlVct[1])
				{
					for(k=0;k<datcount;k++)
					{
						x1.r(1,k+1)=pDoc->m_fDatVct[m_cAnalDlg2.m_iDataSeg][k];
					}
					d1=1;
				}
				else {str.Format("反卷积：在数据段1输入的通道%d无数据！",m_cAnalDlg2.m_iDataSeg);pView->OutText(str);}

				if(m_cAnalDlg2.m_iDataSeg2>=pDoc->m_iCtlVct[0]&&m_cAnalDlg2.m_iDataSeg2<=pDoc->m_iCtlVct[1])
				{
					for(k=0;k<datcount;k++)
					{
						x2.r(1,k+1)=pDoc->m_fDatVct[m_cAnalDlg2.m_iDataSeg2][k];
					}
					d2=1;
				}
				else {str.Format("反卷积：在数据段2输入的通道%d无数据！",m_cAnalDlg2.m_iDataSeg2);pView->OutText(str);}

				if(2==d1+d2)
				{
					y=deconv(x1,x2);

					for (k=0;k<y.cols();k++)
					{  
						fprintf(pFile,"%.4g,",y.r(1,k+1));
					} 

					pDoc->m_iAnalCtl[0]=3;
					pDoc->m_iAnalCtl[1]=m_cAnalDlg2.m_iDataSeg;
					pDoc->m_iAnalCtl[2]=m_cAnalDlg2.m_iDataSeg2;

					pDoc->m_fDatVct[16].clear();
					pDoc->m_fDatVct[16].push_back(0);
					pDoc->m_fDatVct[16].push_back(y.cols()*tlength/datcount);

					pDoc->m_fDatVct[17].clear();
					for(int n=0;n<y.cols();n++)
					{
						pDoc->m_fDatVct[17].push_back(y.r(1,n+1));
					}
				}
					
				fclose(pFile); 

				break;

			case 4:      //DFT分析
				x1=rand(1,datcount);

				if(m_cAnalDlg2.m_iDataSeg>=pDoc->m_iCtlVct[0]&&m_cAnalDlg2.m_iDataSeg<=pDoc->m_iCtlVct[1])
				{
					for(k=0;k<datcount;k++)
					{
						x1.r(1,k+1)=pDoc->m_fDatVct[m_cAnalDlg2.m_iDataSeg][k];
					}
					d1=1;
				}
				else {str.Format("DFT：数据段1输入的通道%d无数据！",m_cAnalDlg2.m_iDataSeg);pView->OutText(str);}

				if(d1)
				{
					y=dft(x1);

					for (k=0;k<y.size();k++)
					{  
						if(0==y.i(1,k+1))fprintf(pFile,"%.4g,",y.r(1,k+1));
						if(0<y.i(1,k+1)) fprintf(pFile,"%.4g+%.4gi,",y.r(1,k+1),y.i(1,k+1));
						else fprintf(pFile,"%.4g%.4gi,",y.r(1,k+1),y.i(1,k+1));
					} 

					pDoc->m_iAnalCtl[0]=4;
					pDoc->m_iAnalCtl[1]=m_cAnalDlg2.m_iDataSeg;
					pDoc->m_iAnalCtl[2]=1280;

					fT=1000.0f/tlength;
					pDoc->m_fDatVct[16].clear();
					pDoc->m_fDatVct[16].push_back(0);
					pDoc->m_fDatVct[16].push_back(fT*pDoc->m_iCtlVct[6]);

					pDoc->m_fDatVct[17].clear();
					pDoc->m_fDatVct[18].clear();
					for(k=0;k<y.cols();k++)
					{
						pDoc->m_fDatVct[17].push_back(y.r(1,k+1));
						pDoc->m_fDatVct[18].push_back(y.i(1,k+1));
					}

				}

					
				fclose(pFile); 

/*				OMG=colon(-(datcount-1)*fT/2.0,fT,(datcount-1)*fT/2.0);
				real=rand(1,datcount);
				nm=rand(1,datcount);
				img=rand(1,datcount);				

				plot((CL(OMG),nm,TM("r")));
				title((CL(TM("DFT_TRANSF"))));
				xlabel((CL(TM("OMG:kHz"))));
				ylabel((CL(TM("Norm Axes: V"))));
*/
				break;

			case 5:      //FFT分析
				x1=rand(1,datcount);

				if(m_cAnalDlg2.m_iDataSeg>=pDoc->m_iCtlVct[0]&&m_cAnalDlg2.m_iDataSeg<=pDoc->m_iCtlVct[1])
				{
					for(k=0;k<datcount;k++)
					{
						x1.r(1,k+1)=pDoc->m_fDatVct[m_cAnalDlg2.m_iDataSeg][k];
					}
					d1=1;
				}
				else {str.Format("FFT:数据段1中输入的通道%d无数据！",m_cAnalDlg2.m_iDataSeg);pView->OutText(str);}
				
				if(d1)
				{
					y=fft(x1);

					for (k=0;k<y.cols();k++)
					{  
						if(0==y.i(1,k+1))fprintf(pFile,"%.4g,",y.r(1,k+1));
						if(0<y.i(1,k+1)) fprintf(pFile,"%.4g+%.4gi,",y.r(1,k+1),y.i(1,k+1));
						else fprintf(pFile,"%.4g%.4gi,",y.r(1,k+1),y.i(1,k+1));
					} 

					pDoc->m_iAnalCtl[0]=5;
					pDoc->m_iAnalCtl[1]=m_cAnalDlg2.m_iDataSeg;
					pDoc->m_iAnalCtl[2]=100099;

					fT=1.0f/tlength;
					pDoc->m_fDatVct[16].clear();
					pDoc->m_fDatVct[16].push_back(0);
					pDoc->m_fDatVct[16].push_back(fT*pDoc->m_iCtlVct[6]);

					pDoc->m_fDatVct[17].clear();
					pDoc->m_fDatVct[18].clear();
					for(k=0;k<y.cols();k++)
					{
						pDoc->m_fDatVct[17].push_back(y.r(1,k+1));
						pDoc->m_fDatVct[18].push_back(y.i(1,k+1));
					}

				}
					
				fclose(pFile); 
				
/*				OMG=colon(-(datcount-1)*fT/2.0,fT,(datcount-1)*fT/2.0);
				real=rand(1,datcount);
				nm=rand(1,datcount);
				img=rand(1,datcount);				
				for(k=1;k<=datcount;k++)
				{
					nm.r(1,k)=sqrt(y.r(1,k)*y.r(1,k)+y.i(1,k)*y.i(1,k));
					real.r(1,k)=y.r(1,k);
					img.r(1,k)=y.i(1,k);
				}

				str.Format("O=%d,r=%d,D=%d",OMG.size(),real.size(),datcount);dc.TextOut(10,10,str);
				mset(gcf(),TM("IconFile"),TM("ArtData.ico"));
				plothandle=winaxes(pView->m_hWnd);
				axesposition(100,100,400,200);
				plothandle=winaxes(pPIC->m_hWnd);
				pos=(BR(100),100,400,200);
				set(plothandle,TM("RealPosition"),pos);
				//plot(((CL(OMG),real,TM("y")),(CL(OMG),img,TM("r")),(CL(OMG),nm,TM("w"))));
				plot((CL(OMG),nm,TM("r")));
				title((CL(TM("FFT_TRANSF"))));
				xlabel((CL(TM("OMG:kHz"))));
				ylabel((CL(TM("Norm Axes: V"))));*/
				break;

			case 6:      //误差erf
				x1=rand(1,datcount);

				if(m_cAnalDlg2.m_iDataSeg>=pDoc->m_iCtlVct[0]&&m_cAnalDlg2.m_iDataSeg<=pDoc->m_iCtlVct[1])
				{
					for(k=0;k<datcount;k++)
					{
						x1.r(1,k+1)=pDoc->m_fDatVct[m_cAnalDlg2.m_iDataSeg][k];
					}
					d1=1;
				}
				else {str.Format("误差函数：数据段1输入的通道%d无数据！",m_cAnalDlg2.m_iDataSeg);pView->OutText(str);}

				if(d1)
				{
					y=erf(x1);

					for (k=0;k<y.cols();k++)
					{  
						fprintf(pFile,"%.4g,",y.r(1,k+1));
					} 

					pDoc->m_iAnalCtl[0]=6;
					pDoc->m_iAnalCtl[1]=m_cAnalDlg2.m_iDataSeg;
					pDoc->m_iAnalCtl[2]=10099;

					pDoc->m_fDatVct[16].clear();
					pDoc->m_fDatVct[16].push_back(0);
					pDoc->m_fDatVct[16].push_back(pDoc->m_iCtlVct[7]);

					pDoc->m_fDatVct[17].clear();
					for(k=0;k<y.cols();k++)
					{
						pDoc->m_fDatVct[17].push_back(y.r(1,k+1));
					}

				}
					
				fclose(pFile); 

				break;

			case 7:      //余误差erfc分析
				x1=rand(1,datcount);

				if(m_cAnalDlg2.m_iDataSeg>=pDoc->m_iCtlVct[0]&&m_cAnalDlg2.m_iDataSeg<=pDoc->m_iCtlVct[1])
				{
					for(k=0;k<datcount;k++)
					{
						x1.r(1,k+1)=pDoc->m_fDatVct[m_cAnalDlg2.m_iDataSeg][k];
					}
					d1=1;
				}
				else {str.Format("余误差：数据段1中输入的通道%d无数据！",m_cAnalDlg2.m_iDataSeg);pView->OutText(str);}

				if(d1)
				{
					y=erfc(x1);

					for (k=0;k<y.cols();k++)
					{  
						fprintf(pFile,"%.4g,",y.r(1,k+1));
					} 

					pDoc->m_iAnalCtl[0]=7;
					pDoc->m_iAnalCtl[1]=m_cAnalDlg2.m_iDataSeg;
					pDoc->m_iAnalCtl[2]=999992;

					pDoc->m_fDatVct[16].clear();
					pDoc->m_fDatVct[16].push_back(0);
					pDoc->m_fDatVct[16].push_back(pDoc->m_iCtlVct[7]);

					pDoc->m_fDatVct[17].clear();
					for(k=0;k<y.cols();k++)
					{
						pDoc->m_fDatVct[17].push_back(y.r(1,k+1));
					}

				}

				fclose(pFile); 

				break;

				case 8:      //均值
				x1=rand(1,datcount);

				if(m_cAnalDlg2.m_iDataSeg>=pDoc->m_iCtlVct[0]&&m_cAnalDlg2.m_iDataSeg<=pDoc->m_iCtlVct[1])
				{
					for(k=0;k<datcount;k++)
					{
						x1.r(1,k+1)=pDoc->m_fDatVct[m_cAnalDlg2.m_iDataSeg][k];
					}
					d1=1;
				}
				else {str.Format("均值：在数据段1中输入的通道%d无数据！",m_cAnalDlg2.m_iDataSeg);pView->OutText(str);}

				if(d1)
				{
					y=mean(x1);

					for (k=0;k<y.cols();k++)
					{  
						fprintf(pFile,"%.4g,",y.r(1,k+1));
					}

				}

				pDoc->m_iAnalCtl[0]=8;
				pDoc->m_iAnalCtl[1]=m_cAnalDlg2.m_iDataSeg;
				pDoc->m_iAnalCtl[2]=999999999999993.00001f/1e-3;

				pDoc->m_fDatVct[16].clear();

				pDoc->m_fDatVct[17].clear();
					
				fclose(pFile); 
				str.Format("通道%d均值：%f",m_cAnalDlg2.m_iDataSeg,y.r(1,1));pView->OutText(str);
				break;

				case 9:      //标准差
				x1=rand(1,datcount);

				if(m_cAnalDlg2.m_iDataSeg>=pDoc->m_iCtlVct[0]&&m_cAnalDlg2.m_iDataSeg<=pDoc->m_iCtlVct[1])
				{
					for(k=0;k<datcount;k++)
					{
						x1.r(1,k+1)=pDoc->m_fDatVct[m_cAnalDlg2.m_iDataSeg][k];
					}
					d1=1;
				}
				else {str.Format("标准差：在数据段1输入的通道%d无数据！",m_cAnalDlg2.m_iDataSeg);pView->OutText(str);}

				if(d1)
				{
					double a;
					y=stdM(x1,0);

					fprintf(pFile,"n-1标准差：%.4g,",y.r(1,1));
					a=y.r(1,1);

					y=stdM(x1,1);

						fprintf(pFile,"n标准差：%.4g,",y.r(1,1));

					pDoc->m_iAnalCtl[0]=9;
					pDoc->m_iAnalCtl[1]=m_cAnalDlg2.m_iDataSeg;
					pDoc->m_iAnalCtl[2]=999999999;


					pDoc->m_fDatVct[16].clear();
					pDoc->m_fDatVct[16].push_back(0);

					pDoc->m_fDatVct[17].clear();
					pDoc->m_fDatVct[17].push_back(a);
					pDoc->m_fDatVct[17].push_back(y.r(1,1));

					fclose(pFile); 
					str.Format("通道%d的n-1标准差：%f；n标准差：%f",m_cAnalDlg2.m_iDataSeg,a,y.r(1,1));pView->OutText(str);
				}
					

				break;

				case 10:      //滤波
				x1=rand(1,datcount);

				if(m_cAnalDlg2.m_iDataSeg>=pDoc->m_iCtlVct[0]&&m_cAnalDlg2.m_iDataSeg<=pDoc->m_iCtlVct[1])
				{
					for(k=0;k<datcount;k++)
					{
						x1.r(1,k+1)=pDoc->m_fDatVct[m_cAnalDlg2.m_iDataSeg][k];
					}
				d1=1;
				}
				else {pView->OutText("数据段1无数据！");}
				
				if(d1)
				{
					Mm a=(1,1,1),b=(2,1,2);

					y=filter(b,a,x1);

					for (k=0;k<y.size();k++)
					{  
						fprintf(pFile,"%.4g,",y.r(1,k+1));
					}

					fclose(pFile);
				}
				break;
			}//switch()
			if(d1||d2)
			{
				str.Format("分析完成，结果保存在Results.ans中！");
				pView->DrawAnal();
			}
			else{str.Format("无法完成");}//OutText(str);

			Invalidate();

		}

		exitM();
	}




}

void CMainFrame::OnUpdateSmplReset(CCmdUI* pCmdUI) 
{
	// TODO: Add your command update UI handler code here
	CArtDataView* pView=(CArtDataView*)GetActiveView();
	if(pView->m_bADWorking){pCmdUI->Enable(FALSE);	}
	
}

void CMainFrame::OnUpdateClear(CCmdUI* pCmdUI) 
{
	// TODO: Add your command update UI handler code here
	CArtDataView* pView=(CArtDataView*)GetActiveView();
	if(pView->m_bADWorking){pCmdUI->Enable(FALSE);}
}


void CMainFrame::OnUpdateSmplStart(CCmdUI* pCmdUI) 
{
	// TODO: Add your command update UI handler code here
	CArtDataView* pView=(CArtDataView*)GetActiveView();
	if(pView->m_bADWorking){pCmdUI->Enable(FALSE);}
	
}

void CMainFrame::OnUpdateAnalsysGen(CCmdUI* pCmdUI) 
{
	// TODO: Add your command update UI handler code here
	CArtDataView* pView=(CArtDataView*)GetActiveView();
	CArtDataDoc* pDoc=pView->GetDocument();
	if(0==pDoc->m_iCtlVct.size()||pView->m_bADWorking){pCmdUI->Enable(FALSE);}

}
