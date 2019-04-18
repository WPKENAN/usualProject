#include "stdafx.h"
#include "ArtData.h"
#include <vector>
using namespace std;
#include "ArtDataView.h"
#include "ClrDatDlg.h"
#include "mmsystem.h"
#pragma comment(lib,"Winmm.lib")
#include <math.h>
#define DOUBLE_PI    6.283185307179586476925286766559
#ifdef _DEBUG
#define new DEBUG_NEW
#undef THIS_FILE
static char THIS_FILE[] = __FILE__;
#endif
#define nIDEvSmp 1
#define nIDEvDrw 2
// ArtDataView.cpp : implementation of the CArtDataView class
//

/////////////////////////////////////////////////////////////////////////////
// CArtDataView

IMPLEMENT_DYNCREATE(CArtDataView, CScrollView)

BEGIN_MESSAGE_MAP(CArtDataView, CScrollView)
	//{{AFX_MSG_MAP(CArtDataView)
	ON_COMMAND(IDM_SMPL_PARM, OnSmplParm)
	ON_COMMAND(IDM_SMPL_DISPLAY, OnSmplDisplay)
	ON_COMMAND(IDM_SMPL_START, OnSmplStart)
	ON_COMMAND(IDM_SMPL_STOP, OnSmplStop)
	ON_WM_TIMER()
	ON_COMMAND(IDM_SMPL_RESET, OnSmplReset)
	ON_WM_KEYDOWN()
	ON_COMMAND(IDM_CLEAR, OnClear)
	ON_WM_DESTROY()
	ON_WM_MOVE()
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CArtDataView construction/destruction

CArtDataView::CArtDataView()
{
	// TODO: add construction code here
		m_bCurvDisp=TRUE;
		m_bDeviceWorking=FALSE;
		m_bADWorking=FALSE;
		m_bTimerSmp=FALSE;
		m_bTimerDrw=FALSE;
		m_bSmpFlag=FALSE;
		m_bDrwFlag=FALSE;
		m_bByMembFun=FALSE;
		m_bEnableOutText=FALSE;

		m_sOutText[0]="欢迎使用ArtData 1.0系统!";
		m_sOutText[1]="系统每通道最高采样率:单通道12.5KHz,多通道4.167KHz.";
	m_sOutText[2]="可以开始数据采集，也可以打开*.art文件";
	m_sOutText[3]="内存中有数据后即可以进行分析，结果保存在Results.ans文件中";
	m_sOutText[4]="版本升级中...";

	m_sCdParm.FirstChannel=0;
	m_sCdParm.Gains=0;
	m_sCdParm.GroundingMode=0;
	m_sCdParm.InputRange=0;
	m_sCdParm.LastChannel=0;

	m_iSmplFrq=0;
	m_iSmplTime=3600;//默认采样时长
	m_fAmplfV=1.0f;  //z纵坐标显示放大系数
//	m_fAmplfT=1.0f; //横坐标抽样间距
	m_uElpDrw=15; //绘图周期
	m_uElpSmp=125;//采样周期，实际值在OnSmpStart()中计算
	m_wAccuracy=1;

	m_iChAmount[0]=16;
	m_iChAmount[1]=8;

	m_iTotalDispTimeCapUs=(float)m_uElpDrw/256.0f*650.0; //横坐标的时宽总标度
	//m_iStartTimes=0;
	//m_iStopTimes=0;
//	m_fTime=0;
	m_pCdDlg=new CCardDlg();
	memset(&m_sCdParm,0,sizeof(m_sCdParm));
	m_hDevice=NULL;

//	m_TextPosX=20;
//	m_TextPosY=10;

	m_clientSize=CSize(250,455);
//	for(int i=0;i<8192;i++){m_nADBuffer[i]=0;}

	m_cAnalDC.CreateCompatibleDC(NULL); 
	CBitmap MemBitmap;
	MemBitmap.CreateCompatibleBitmap(&m_cAnalDC,992,2900);	//创建一个内存中的图像		
	//CPen PenForDrawAB(PS_SOLID, 1, RGB(0,98,0));
	m_cAnalDC.SelectObject(&MemBitmap); 		//指定内存显示设备在内存中的图像上画图

}

CArtDataView::~CArtDataView()
{
OnSmplStop();OnClear();m_cAnalDC.DeleteDC();
/*	timeEndPeriod(m_wAccuracy);
	if(m_bTimerSmp=TRUE){timeKillEvent(m_TimerIDSmp);}
	if(m_bTimerDrw=TRUE)timeKillEvent(m_TimerIDDrw);
	
	if(m_bADWorking==TRUE)
	{
		if(!USB5935_ReleaseDeviceAD(m_hDevice)){MessageBox("无法关闭AD设备");}
		else{m_bADWorking=FALSE;}
	}
	if(m_bDeviceWorking==TRUE)
	{
		if(!USB5935_ReleaseDevice(m_hDevice)){MessageBox("无法关闭设备");}
		else{m_bDeviceWorking=FALSE;}
	}
*/
}

BOOL CArtDataView::PreCreateWindow(CREATESTRUCT& cs)
{
	// TODO: Modify the Window class or styles here by modifying
	//  the CREATESTRUCT cs

	return CScrollView::PreCreateWindow(cs);
}

void PASCAL SampDataProc(UINT wTimerID, UINT msg,DWORD dwUser,DWORD dwl,DWORD dw2) 
{ 
	CMainFrame* pMainFrame=(CMainFrame*)AfxGetMainWnd();
	CArtDataView* pView=(CArtDataView*)pMainFrame->GetActiveView();
//	pView->ReadCard();
	pView->m_bSmpFlag=TRUE;
}

void PASCAL DrawDataProc(UINT wTimerID, UINT msg,DWORD dwUser,DWORD dwl,DWORD dw2) 
{ 
	CMainFrame* pMainFrame=(CMainFrame*)AfxGetMainWnd();
	CArtDataView* pView=(CArtDataView*)pMainFrame->GetActiveView();

	CDC *pDC=pView->GetDC();

	pView->m_bByMembFun=TRUE;
	pView->OnDraw(pDC);
//	pView->m_bDrwFlag=TRUE;

}
/////////////////////////////////////////////////////////////////////////////
// CArtDataView drawing

void CArtDataView::ReadCard()
{
	// TODO: Add your message handler code here and/or call default
	DWORD USB5935_GetLastErrorEx(LPCSTR strFuncName,LPCSTR strErrorMsg);
	DWORD dwErrorCode;
	CString str;
	char strErrorMsg[256];
	int i,chnl,DCountPerChnl;
	static int iFirstChnl,iLastChnl,iInputRange,nChnlCount,iFstCor=0;

//	CClientDC dc(this);
	CArtDataDoc* pDoc=GetDocument();

	if(GetTickCount()-m_dwStartTimeUs>=m_iSmplTime*1000)                                            //设定的采样时间到
	{
		OnSmplStop();
		goto ext;//m_dwStartTimeUs=GetTickCount();
	}  	//Invalidate();	

	else if(m_bDeviceWorking==TRUE&&m_bADWorking==TRUE)
	{
		if(!USB5935_ReadDeviceAD(m_hDevice,m_nADBuffer,m_nReadSizeWords,&m_nRetSizeWords))
		{
			//dwErrorCode = USB5935_GetLastErrorEx("USB5935_InitDeviceAD", strErrorMsg);
			//str.Format("dwErrorCode = %x, %s\n", dwErrorCode, strErrorMsg);
			MessageBox(str);
			OnSmplStop();
		}
		else if(m_nReadSizeWords==m_nRetSizeWords)
		{
			if(m_bNewSmpParm)//采样新参数，在OnSmplStart()中更新
			{
				m_bNewSmpParm=FALSE;
				iFirstChnl=m_sCdParm.FirstChannel;
				iLastChnl=m_sCdParm.LastChannel;
				iInputRange=m_sCdParm.InputRange;
				iFstCor=1;
				nChnlCount=iLastChnl+1;
			}
			else{iFstCor=0;}
			DCountPerChnl=m_nRetSizeWords/nChnlCount;
			switch(iInputRange)
			{
			case 0:
				for(chnl=iFirstChnl;chnl<=iFirstChnl+iLastChnl;chnl++)
				{
					//if(pDoc->m_fDatVct[chnl].capacity()-pDoc->m_dwDatIndex[chnl]<DCountPerChnl)
					//{pDoc->m_fDatVct[chnl].resize(pDoc->m_dwDatIndex[chnl]+DCountPerChnl*1024);}
					for(i=0;i<DCountPerChnl;i++)
					{
//						pDoc->m_fDatVct[chnl][pDoc->m_dwDatIndex[chnl]]=20.0*(m_nADBuffer[i*nChnlCount+chnl+iFstCor]&0x1fff)/8192-10.0;
						//pDoc->m_dwDatIndex[chnl]++;
						float a=20.0*(m_nADBuffer[i*nChnlCount+chnl+iFstCor]&0x1fff)/8192-10.0;
						pDoc->m_fDatVct[chnl].push_back(a);
						//str.Format("%2.2f,",a);	dc.TextOut((i%12)*50+80,80,str);
					}
				}
				break;
			case 1:
				for(chnl=iFirstChnl;chnl<=iFirstChnl+iLastChnl;chnl++)
				{
					//if(pDoc->m_fDatVct[chnl].capacity()-pDoc->m_dwDatIndex[chnl]<DCountPerChnl)
					//{pDoc->m_fDatVct[chnl].resize(pDoc->m_dwDatIndex[chnl]+DCountPerChnl*1024);}
					for(i=0;i<DCountPerChnl;i++)
					{
						pDoc->m_fDatVct[chnl].push_back(10.0*(m_nADBuffer[i*nChnlCount+chnl+iFstCor]&0x1fff)/8192-5.0);
						//pDoc->m_dwDatIndex[chnl]++;
					}
				}
				break;
			case 2:
				for(chnl=iFirstChnl;chnl<=iFirstChnl+iLastChnl;chnl++)
				{
					//if(pDoc->m_fDatVct[chnl].capacity()-pDoc->m_dwDatIndex[chnl]<DCountPerChnl)
					//{pDoc->m_fDatVct[chnl].resize(pDoc->m_dwDatIndex[chnl]+DCountPerChnl*1024);}
					for(i=0;i<DCountPerChnl;i++)
					{
						pDoc->m_fDatVct[chnl].push_back(5.0*(m_nADBuffer[i*nChnlCount+chnl+iFstCor]&0x1fff)/8192-2.50);
						//pDoc->m_dwDatIndex[chnl]++;
					}
				}
				break;
			case 3:
				for(chnl=iFirstChnl;chnl<=iFirstChnl+iLastChnl;chnl++)
				{
					//if(pDoc->m_fDatVct[chnl].capacity()-pDoc->m_dwDatIndex[chnl]<DCountPerChnl)
					//{pDoc->m_fDatVct[chnl].resize(pDoc->m_dwDatIndex[chnl]+DCountPerChnl*1024);}
					for(i=0;i<DCountPerChnl;i++)
					{
						pDoc->m_fDatVct[chnl].push_back(10.0*(m_nADBuffer[i*nChnlCount+chnl+iFstCor]&0x1fff)/8192);
						//pDoc->m_dwDatIndex[chnl]++;
					}
				}	
			}//switch(m_sCdParm.InputRange)
			pDoc->m_iDatPtr=pDoc->m_fDatVct[chnl].size()-1;
		}
		
		else{MessageBox("读失败！");}
	}//if(m_bDeviceWorking==TRUE&&m_bADWorking==TRUE)
ext:;
}

void CArtDataView::DrawData()
{	
/*	CArtDataDoc* pDoc = GetDocument();
//	ASSERT_VALID(pDoc);
	static int counts=0;
		DWORD 	t1=GetTickCount();
				
		int PicWidth=650,PicHeigh=250,PicPosX=50,PicPosY=120;
		int OriginOfY=PicHeigh/2;

	if(TRUE==m_bADWorking)
	{
		counts++;		

		CDC *pDC = GetDC();
		//创建一个内存中的显示设备
		CDC MemDC;
		MemDC.CreateCompatibleDC(NULL); 
		CBitmap MemBitmap;
		MemBitmap.CreateCompatibleBitmap(pDC,PicWidth+200,PicHeigh);	//创建一个内存中的图像		
		CPen *pNewPen,*pOldPen;//定义各种类型的画笔
		//CPen PenForDrawAB(PS_SOLID, 1, RGB(0,98,0));
		MemDC.SelectObject(&MemBitmap); 		//指定内存显示设备在内存中的图像上画图
		//先用一种颜色作为内存显示设备的背景色
		MemDC.FillSolidRect(0,0,PicWidth+200,PicHeigh,RGB(20,20,20));
		//MemDC.SetBkColor(RGB(2,2,250));

		//if(DatPt[10].x!=DatPt[10].x)
		static int iFirstChnl=0,iLastChnl=0,iInputRange=0;
		static int iColorIndex[][3]={{255,128,128},{255,255,128},{128,255,128},{128,255,255},{0,128,255},
		{255,128,255},{0,128,128},{128,0,128},{64,64,128},{128,64,128},{128,0,0},{255,128,0},{255,128,255},{128,0,0},{128,64,64},{255,255,255}};
		static POINT DatPt[650]={0};
		static POINT GridPt[48],LegendPt[48];
		float InputRange[][2]={{-10,20},{-5,10},{-2.5,5},{0,10}};
//		float m_iTotalDispTimeCapUs=1000.0;
		float fVctSmpCor,f;
		int iCurrentDatPt=0,iTotalDispCount,iDatVctSize=0,i,chnl;
		CString str;

		if(m_bFirstSmp)//开始按钮单击
		{
			m_bFirstSmp=FALSE;
			iFirstChnl=m_sTmpParm.FirstChannel;
			iLastChnl=m_sTmpParm.LastChannel;
			iInputRange=m_sTmpParm.InputRange;

			for(i=0;i<=PicWidth;i++)//曲线的横坐标
			{	DatPt[i].x=PicWidth-i;	}
			int a=-1;////////////网格线的点
			for(i=0;i<18;i+=2)
			{
				a*=-1;
				GridPt[i].x=PicWidth/2-a*PicWidth/2;
				GridPt[i].y=i*PicHeigh/16;
				a*=-1;
				GridPt[i+1].x=PicWidth/2-a*PicWidth/2;
				GridPt[i+1].y=i*PicHeigh/16;
				a*=-1;
			}
			for(;i<=40;i+=2)
			{
				a*=-1;
				GridPt[i].y=PicHeigh/2-a*PicHeigh/2;
				GridPt[i].x=PicWidth-(i-18)*PicWidth/20;
				a*=-1;
				GridPt[i+1].y=PicHeigh/2-a*PicHeigh/2;
				GridPt[i+1].x=PicWidth-(i-18)*PicWidth/20;
				a*=-1;
			}
			for(int ch=0;ch<16;ch++)
			{
				LegendPt[3*ch].x=PicWidth+68;  LegendPt[3*ch].y=PicHeigh-240+ch*PicHeigh/17;
				LegendPt[3*ch+1].x=PicWidth+60;LegendPt[3*ch+1].y=PicHeigh-240+ch*PicHeigh/17;
				LegendPt[3*ch+2].x=PicWidth+60;LegendPt[3*ch+2].y=PicHeigh-240+(ch+1)*PicHeigh/17;
			}

		}
///////////////绘制网格及坐标
		pNewPen=new CPen;
		pNewPen->CreatePen(PS_DOT,1,RGB(255,255,0));
		pOldPen=MemDC.SelectObject(pNewPen);
		MemDC.Polyline(GridPt,40);
		MemDC.Polyline(LegendPt,47);
		MemDC.SelectObject(pOldPen);
		delete pNewPen;

		float a=((float)(m_iTotalDispTimeCapUs)/10000.0);
		int k=0;
		while(a<0.1f){a*=10.0f;k--;}
		while(a>1.00f){a/=10.0f;k++;}
		for(i=1;i<10;i++)
		{
			str.Format("%.2f",i*a);
			pDC->TextOut(PicPosX+i*PicWidth/10-8,PicPosY+PicHeigh,str);
		}
		str.Format("10^%ds",k);
		pDC->TextOut(PicPosX+i*PicWidth/10-16,PicPosY+PicHeigh,str);
		for(i=1;i<8;i++)
		{
			str.Format("%1.1f",i*InputRange[iInputRange][1]/8+InputRange[iInputRange][0]);
			pDC->TextOut(PicPosX-26,PicPosY+PicHeigh-i*PicHeigh/8-8,str);
		}
		pDC->TextOut(PicPosX-13,PicPosY+PicHeigh-i*PicHeigh/8,"V");
////////////////////////		
		iTotalDispCount=(int)(256.0/(float)m_uElpSmp*m_iTotalDispTimeCapUs);
		fVctSmpCor=(float)iTotalDispCount/(float)PicWidth;//数据到窗口的映射系数

		if(m_bDeviceWorking==TRUE&&m_bADWorking==TRUE)
		for(chnl=iFirstChnl;chnl<=(iFirstChnl+iLastChnl);chnl++)
		{
			int R=iColorIndex[chnl][0],G=iColorIndex[chnl][1],B=iColorIndex[chnl][2];
			pNewPen=new CPen;
			pNewPen->CreatePen(PS_SOLID,1,RGB(R,G,B));
			pOldPen=MemDC.SelectObject(pNewPen);
			POINT DatPtIn[]={{PicWidth+10,PicHeigh-240+chnl*PicHeigh/17},
									{PicWidth+50,PicHeigh-240+chnl*PicHeigh/17}};
			MemDC.Polyline(DatPtIn,2);

			iDatVctSize=pDoc->m_fDatVct[chnl].size();//>m_dwDatIndex[chnl];
			iCurrentDatPt=(iDatVctSize<iTotalDispCount?iDatVctSize:iTotalDispCount);
			if(iCurrentDatPt>fVctSmpCor&&iCurrentDatPt<iTotalDispCount)//数据数目未满但足够显示
			{
				POINT DatPtu[650];
				for(f=0.0,i=0;f<iCurrentDatPt;f+=fVctSmpCor,i++)
				{	
					DatPtu[i].x=i;
					DatPtu[i].y=PicHeigh-PicHeigh*(pDoc->m_fDatVct[chnl][iDatVctSize-iCurrentDatPt+(int)f]
						-InputRange[iInputRange][0])/InputRange[iInputRange][1];
				}
				MemDC.Polyline(DatPtu,i);
			}
			else
			{//			MemDC.MoveTo(DatPt[0].x,OriginOfY*(1-pDoc->m_fDatVct[chnl][iDatVctSize-iCurrentDatPt]));
				for(f=0.0,i=0;f<iCurrentDatPt;f+=fVctSmpCor,i++)
				{
					DatPt[i].y=PicHeigh-PicHeigh*(pDoc->m_fDatVct[chnl][iDatVctSize-iCurrentDatPt+(int)f]
						-InputRange[iInputRange][0])/InputRange[iInputRange][1];
				}
			
				MemDC.Polyline(DatPt,i);
			}

			MemDC.SelectObject(pOldPen);
			delete pNewPen;
		}
				pDC->BitBlt(PicPosX,PicPosY,PicWidth+200,PicHeigh+20, &MemDC, 0, 0, SRCCOPY); 
		
			int seg=pDocm_dwCtlVct[chnl][8];
			str.Empty();
			str.Format("Sampling For %2.2f.%3.3",chnl,seg);
 			pDC->TextOut(300,40,str);
		
		ReleaseDC(pDC);
	}*/
}

void CArtDataView::OnDraw(CDC* pDC)
{
	CArtDataDoc* pDoc = GetDocument();
	ASSERT_VALID(pDoc);
	// TODO: add draw code for native data here

//	ASSERT_VALID(pDoc);
	DWORD 	t1=GetTickCount();

//	static CString;
	static int textposx=10;

	
	pDC->TextOut(textposx,10,m_sOutText[0]);
	pDC->TextOut(textposx,30,m_sOutText[1]);
	pDC->TextOut(textposx,50,m_sOutText[2]);
	pDC->TextOut(textposx,70,m_sOutText[3]);
	pDC->TextOut(textposx,90,m_sOutText[4]);


	int PicWidth=650,PicHeigh=250,PicPosX=50,PicPosY=120;
	int OriginOfY=PicHeigh/2;

		//创建一个内存中的显示设备
	CDC MemDC;
	MemDC.CreateCompatibleDC(NULL); 
	CBitmap MemBitmap;
	MemBitmap.CreateCompatibleBitmap(pDC,PicWidth+200,PicHeigh);	//创建一个内存中的图像		
	CPen *pNewPen,*pOldPen;//定义各种类型的画笔
	//CPen PenForDrawAB(PS_SOLID, 1, RGB(0,98,0));
	MemDC.SelectObject(&MemBitmap); 		//指定内存显示设备在内存中的图像上画图
	//先用一种颜色作为内存显示设备的背景色
	MemDC.FillSolidRect(0,0,PicWidth+200,PicHeigh,RGB(20,20,20));
	//MemDC.SetBkColor(RGB(2,2,250));

	static int iFirstChnl=0,iLastChnl=0,iInputRange=0;
	static int iColorIndex[][3]={{255,128,128},{255,255,128},{128,255,128},{128,255,255},{0,128,255},
	{255,128,255},{0,128,128},{128,0,128},{64,64,128},{128,64,128},{128,0,0},{255,128,0},{255,128,255},{128,0,0},{128,64,64},{255,255,255}};
	static POINT DatPt[650]={0};         //保存数据坐标
	static POINT GridPt[48],LegendPt[48];
	float InputRange[][2]={{-10,20},{-5,10},{-2.5,5},{0,10}};

	float fVctSmpCor;
	int iCurrentDatPt=0,iTotalDispCount,iDatVctSize=0,i,chnl;
	CString str;

	for(i=0;i<=PicWidth;i++)//曲线的横坐标   PicWidth-
	{	DatPt[i].x=i;	}
			
	int a=-1;////////////网格线的点
	for(i=0;i<18;i+=2)
	{
		a*=-1;
		GridPt[i].x=PicWidth/2-a*PicWidth/2;
		GridPt[i].y=i*PicHeigh/16;
		a*=-1;
		GridPt[i+1].x=PicWidth/2-a*PicWidth/2;
		GridPt[i+1].y=i*PicHeigh/16;
		a*=-1;
	}
	for(;i<=40;i+=2)
	{
		a*=-1;
		GridPt[i].y=PicHeigh/2-a*PicHeigh/2;
		GridPt[i].x=PicWidth-(i-18)*PicWidth/20;
		a*=-1;
		GridPt[i+1].y=PicHeigh/2-a*PicHeigh/2;
		GridPt[i+1].x=PicWidth-(i-18)*PicWidth/20;
		a*=-1;
	}
	for(int ch=0;ch<16;ch++)
	{
		LegendPt[3*ch].x=PicWidth+68;  LegendPt[3*ch].y=PicHeigh-240+ch*PicHeigh/17;
		LegendPt[3*ch+1].x=PicWidth+60;LegendPt[3*ch+1].y=PicHeigh-240+ch*PicHeigh/17;
		LegendPt[3*ch+2].x=PicWidth+60;LegendPt[3*ch+2].y=PicHeigh-240+(ch+1)*PicHeigh/17;
	}

///////////////绘制网格及坐标
	pNewPen=new CPen;
	pNewPen->CreatePen(PS_DOT,1,RGB(255,255,0));
	pOldPen=MemDC.SelectObject(pNewPen);
	MemDC.Polyline(GridPt,40);
	MemDC.Polyline(LegendPt,47);
	MemDC.SelectObject(pOldPen);
	delete pNewPen;

	float a_h=(float)m_iTotalDispTimeCapUs;  //显示时宽，该参数可调
	int k=-4;  //标度值指数
	while(a_h<0.1f){a_h*=10.0f;k--;}
	while(a_h>1.00f){a_h/=10.0f;k++;}
	for(i=1;i<10;i++)   //横坐标的标度值
	{
		str.Format("%.2f",i*a_h);
		pDC->TextOut(PicPosX+i*PicWidth/10-8,PicPosY+PicHeigh,str);
	}
	str.Format("  t(10^%d s)",k);
	pDC->TextOut(PicPosX+i*PicWidth/10-16,PicPosY+PicHeigh,str);

	iInputRange=m_sCdParm.InputRange;
	for(i=1;i<8;i++)  //纵坐标的值 
	{
		str.Format("%1.1f",(i*InputRange[iInputRange][1]/8+InputRange[iInputRange][0])/m_fAmplfV);
		pDC->TextOut(PicPosX-26,PicPosY+PicHeigh-i*PicHeigh/8-8,str);
	}
	pDC->TextOut(PicPosX-13,PicPosY+PicHeigh-i*PicHeigh/8,"V");
///////////////////////完成网格及标尺绘制
	 		
	iTotalDispCount=(int)(256.0/(float)m_uElpSmp*m_iTotalDispTimeCapUs);// 窗口时长所包含的通道数据点数
	fVctSmpCor=(float)iTotalDispCount/(float)PicWidth;//数据到窗口的映射系数

	if(pDoc->m_iCtlVct.size())
	{
		for(chnl=pDoc->m_iCtlVct[0];chnl<=pDoc->m_iCtlVct[1];chnl++)
		{
			for(int i=0;(pDoc->m_iDatPtr-i*fVctSmpCor>=0)&&(i*fVctSmpCor<=iTotalDispCount);i++)
			{
				//DatPt[i].y=pDoc->m_fDatVct[chnl][pDoc->m_iDatPtr-i*fVctSmpCor];
				int iDatIndex=pDoc->m_iDatPtr-i*fVctSmpCor;
				double temp=pDoc->m_fDatVct[chnl][iDatIndex];
				for(int k=1;(k<floor(fVctSmpCor)+1)&&iDatIndex-k>=0;k++)
				{
					if(abs(temp)<abs(pDoc->m_fDatVct[chnl][iDatIndex-k]))
					{temp=pDoc->m_fDatVct[chnl][iDatIndex-k];};
				}
				float InpBotm=InputRange[chnl][0];
				float InpRang=InputRange[chnl][1];
				DatPt[i].y=PicHeigh-PicHeigh*(m_fAmplfV*temp-InpBotm)/InpRang;
			}

			pNewPen=new CPen;
			int R=iColorIndex[chnl][0],G=iColorIndex[chnl][1],B=iColorIndex[chnl][2];
			pNewPen->CreatePen(PS_SOLID,1,RGB(R,G,B));
			pOldPen=MemDC.SelectObject(pNewPen);
			MemDC.Polyline(DatPt,i);

			POINT DatPtIn[]={{PicWidth+10,PicHeigh-240+(chnl)*PicHeigh/17},
								{PicWidth+50,PicHeigh-240+(chnl)*PicHeigh/17}};
			MemDC.Polyline(DatPtIn,2);////////画图例

			MemDC.SetTextColor(RGB(R,G,B));	
			str.Format("%2.6g",pDoc->m_fDatVct[chnl][pDoc->m_iDatPtr]);
			MemDC.TextOut(PicWidth+80,PicHeigh-250+(chnl)*PicHeigh/17,str);

			MemDC.SelectObject(pOldPen);
			delete pNewPen;

		}
	}
		   
	pDC->BitBlt(PicPosX,PicPosY,PicWidth+200,PicHeigh+20, &MemDC, 0, 0, SRCCOPY);
	MemDC.DeleteDC();

	if(0!=pDoc->m_fDatVct[17].size())
	{
		int type=pDoc->m_iAnalCtl[0];
		if(0==type||3==type||6==type||7==type)
		{
			pDC->BitBlt(0,PicPosY+360,PicWidth+332,PicHeigh+50, &m_cAnalDC, 0, 0, SRCCOPY);
		}//PicWidth=650,PicHeigh=250,PicPosX=50,PicPosY=120;
		else if(4==type||5==type)
		{
			pDC->BitBlt(0,PicPosY+360,PicWidth+332,PicHeigh*6, &m_cAnalDC, 0, 0, SRCCOPY);
		}
	}


	if(m_bByMembFun)
	{
		ReleaseDC(pDC);
		m_bByMembFun=FALSE;
	}

}

void CArtDataView::OnInitialUpdate()
{
	CScrollView::OnInitialUpdate();

	CSize sizeTotal;
	// TODO: calculate the total size of this view
	sizeTotal.cx = sizeTotal.cy = 100;
	SetScrollSizes(MM_TEXT, sizeTotal);	
	SetScrollSizes(MM_TEXT, m_clientSize);//
}

/////////////////////////////////////////////////////////////////////////////
// CArtDataView diagnostics

#ifdef _DEBUG
void CArtDataView::AssertValid() const
{
	CScrollView::AssertValid();
}

void CArtDataView::Dump(CDumpContext& dc) const
{
	CScrollView::Dump(dc);
}

CArtDataDoc* CArtDataView::GetDocument() // non-debug version is inline
{
	ASSERT(m_pDocument->IsKindOf(RUNTIME_CLASS(CArtDataDoc)));
	return (CArtDataDoc*)m_pDocument;
}
#endif //_DEBUG


void CArtDataView::OnSmplParm() //参数设置对话框？
{
	// TODO: Add your command handler code here
	if(m_pCdDlg->m_bCdDlgShown==FALSE)
	{

	m_pCdDlg->Create(IDD_CARDDLG,this);

	CString str;

	m_pCdDlg->m_cFirstChnnl.SetCurSel(m_sCdParm.FirstChannel);
	m_pCdDlg->m_cSignlGain.SetCurSel(m_sCdParm.Gains);
	m_pCdDlg->m_cSignlGrnd.SetCurSel(m_sCdParm.GroundingMode);
	m_pCdDlg->m_cSignlRng.SetCurSel(m_sCdParm.InputRange);
	m_pCdDlg->m_cSmplFrq.SetCurSel(m_iSmplFrq);
	m_pCdDlg->SetDlgItemInt(IDC_SMPL_TIME,m_iSmplTime);

	((CComboBox*)m_pCdDlg->GetDlgItem(IDC_LST_CHNNL))->ResetContent();
	for(int i=m_sCdParm.FirstChannel;i<m_iChAmount[m_pCdDlg->m_cSignlGrnd.GetCurSel()];i++)
 	{
		//str.Empty();
		str.Format("%d",i);
		((CComboBox*)m_pCdDlg->GetDlgItem(IDC_LST_CHNNL))->AddString(str);
 	}
	m_pCdDlg->m_cLastChnnl.SetCurSel(m_sCdParm.LastChannel);

	m_pCdDlg->ShowWindow(SW_SHOW);
	m_pCdDlg->m_bCdDlgShown=TRUE;
	}
}

void CArtDataView::OnSmplDisplay() 
{
	// TODO: Add your command handler code here
	if(FALSE==m_bCurvDisp)
	{
		m_bCurvDisp=TRUE;
	}
	else
	{
		m_bCurvDisp=FALSE;
	}	
}

void CALLBACK TimerProc(HWND hWnd,UINT nMsg,UINT nTimerid,DWORD dwTime)
{
	CMainFrame* pMainFrame=(CMainFrame*)AfxGetMainWnd();
	CArtDataView* pView=(CArtDataView*)pMainFrame->GetActiveView();
	MSG msg;
//	pView->ReadCard();
	pView->KillTimer(1);
	
//	DWORD t1=GetTickCount();
	for(;pView->m_bDeviceWorking==TRUE&&pView->m_bADWorking==TRUE;)
	{
		if(pView->m_bSmpFlag==TRUE){pView->ReadCard();pView->m_bSmpFlag=FALSE;}
		if (PeekMessage (&msg, NULL, 0, 0, PM_REMOVE))  //
        {
			if (msg.message == WM_QUIT||msg.message==WM_COMMAND)//WM_LBUTTONDOWN)
            TranslateMessage (&msg) ;
            DispatchMessage (&msg) ; 
			   
		}

//		if(m_bDrwFlag==TRUE){DrawData();m_bDrwFlag=FALSE;}
//		if(GetTickCount()-t1>20){ReadCard();DrawData();		t1=GetTickCount();
//}
	}
}

void CArtDataView::OnTimer(UINT nIDEvent) //定时器2的响应函数，进入后清除定时器，无限循环中根据是否有采样标志m_bSmpFlag进行采样
{
	KillTimer(2);
	CString str;
	MSG msg;
//	CClientDC dc(this);		
	for(;m_bDeviceWorking==TRUE&&m_bADWorking==TRUE;)
	{//waitforsingleobject()

		if(PeekMessage (&msg,NULL,0,0,PM_REMOVE))  //
        {
			if(msg.message==WM_QUIT||msg.message==WM_COMMAND)
			{OnSmplStop();break;}
			else {TranslateMessage (&msg) ;
			DispatchMessage (&msg) ;}
        }

		if(m_bSmpFlag==TRUE)
		{		
			DWORD t1=GetTickCount();
			ReadCard();
			m_bSmpFlag=FALSE;
			//str.Format("本次采样耗时:%4.4d 毫秒",GetTickCount()-t1);	
		}

//		if(GetTickCount()-t1>20){ReadCard();DrawData();		t1=GetTickCount();
//}
	}
//	CScrollView::OnTimer(nIDEvent);
}

void CArtDataView::OnSmplStart() 
{
	// TODO: Add your command handler code here
	CString str;
	float fCorFrq[]={1.0f,1.0f,0.8f,0.6f,0.4f,0.2f};
	CArtDataDoc* pDoc=GetDocument();

	if(FALSE==m_bDeviceWorking)
	{
		CArtDataDoc* pDoc=GetDocument();
		BOOL DocIsEmpty=1;
		for(int chnl=0;chnl<16;chnl++)
		{
			if(pDoc->m_fDatVct[chnl].size()!=0) DocIsEmpty=0;
		}
		if(!DocIsEmpty)
		{
			CClrDatDlg clrdatDlg;
			
			switch(clrdatDlg.DoModal())
			{
			case IDOK:
				OnClear();
				if(pDoc->m_bFromFile){pDoc->m_bFromFile=FALSE;}
				str.Format("通道数据已清除！");
				OutText(str);
				break;
			case IDCANCEL:
				str.Format("请先保存通道数据！");
				goto ext;
			}
		}
		m_hDevice=USB5935_CreateDevice(0);   //启动设备
		if(INVALID_HANDLE_VALUE==m_hDevice){MessageBox("无法创建设备");}
		else{m_bDeviceWorking=TRUE;}
	}

	char strErrorMsg[256];
	DWORD dwErrorCode;
	TIMECAPS tc; //利用函数timeGetDeVCaps取出系统分辨率的取值范围，如果无错则继续； 

	if(TRUE==m_bDeviceWorking&&!m_bADWorking)                //启动AD和定时器
	{
		if(0==m_sCdParm.LastChannel){m_uElpSmp=20.0/fCorFrq[m_iSmplFrq];}     
		else {m_uElpSmp=(m_sCdParm.LastChannel+1)*60.0/fCorFrq[m_iSmplFrq];}

		m_nReadSizeWords=256*(m_sCdParm.LastChannel+1);//*nCorReadSize[m_iSmplFrq];

		if(!USB5935_InitDeviceAD(m_hDevice,&m_sCdParm))
		{
			//dwErrorCode = USB5935_GetLastErrorEx("USB5935_InitDeviceAD", strErrorMsg);
			//str.Format("错误!dwErrorCode = %x, %s\n", dwErrorCode, strErrorMsg);
			MessageBox(str);
		}
		else 
		{//	m_dwStartTimeUs=GetTickCount();
			m_bADWorking=TRUE;   
			SetTimer(2,10,NULL);   //绘图定时器
			//Sleep(100);
			if(m_bDeviceWorking&&m_bADWorking&&m_bTimerSmp==FALSE&&m_bTimerDrw==FALSE)
			{
				if(timeGetDevCaps(&tc,sizeof(TIMECAPS))==TIMERR_NOERROR) 
				{ 
					m_wAccuracy=min(max(tc.wPeriodMin,m_wAccuracy),tc.wPeriodMax);
					timeBeginPeriod(m_wAccuracy); 
					if(1)
					{   m_bNewSmpParm=TRUE;
						if(InitializeTimer()){m_bTimerSmp=TRUE; m_bTimerDrw=TRUE;}
						//if(0==m_iStartTimes)
						{m_dwStartTimeUs=GetTickCount();		}
					}
				}
			}
		}

		//m_bFirstSmp=TRUE;
		m_sTmpParm.FirstChannel=m_sCdParm.FirstChannel;
		m_sTmpParm.Gains=m_sCdParm.Gains;
		m_sTmpParm.GroundingMode=m_sCdParm.GroundingMode;
		m_sTmpParm.InputRange=m_sCdParm.InputRange;
		m_sTmpParm.LastChannel=m_sCdParm.LastChannel;

			pDoc->m_iCtlVct.push_back((long)m_sTmpParm.FirstChannel);//本段的首通道号LONG			long lstch=;
			pDoc->m_iCtlVct.push_back((long)m_sTmpParm.FirstChannel+m_sTmpParm.LastChannel);//末通道号LONG			long gn=;
			pDoc->m_iCtlVct.push_back((long)m_sTmpParm.Gains);//本段的增益       LONG			long grnd=;
			pDoc->m_iCtlVct.push_back((long)m_sTmpParm.GroundingMode);//本段接地 LONG			long inprg=;
			pDoc->m_iCtlVct.push_back((long)m_sTmpParm.InputRange);//本段输入电压范围           LONG: 0~3			long elp=;
			pDoc->m_iCtlVct.push_back((long)m_uElpSmp);//本段采样周期             UINT			long siz=;

			//m_segStartTimeUs=GetTickCount()-m_dwStartTimeUs;
		//m_iStartTimes++;
/*		GetParent()->GetMenu()->GetSubMenu(0)->EnableMenuItem(ID_FILE_NEW, MF_BYCOMMAND| MF_DISABLED|MF_GRAYED);
		GetParent()->GetMenu()->GetSubMenu(0)->EnableMenuItem(ID_FILE_OPEN, MF_BYCOMMAND| MF_DISABLED|MF_GRAYED);
		GetParent()->GetMenu()->GetSubMenu(0)->EnableMenuItem(ID_FILE_SAVE, MF_BYCOMMAND| MF_DISABLED|MF_GRAYED);
		GetParent()->GetMenu()->GetSubMenu(0)->EnableMenuItem(ID_FILE_SAVE_AS, MF_BYCOMMAND| MF_DISABLED|MF_GRAYED);

		GetParent()->GetMenu()->GetSubMenu(1)->EnableMenuItem(0, MF_BYPOSITION| MF_DISABLED|MF_GRAYED);*/
	
	char gain[4];
	char grnd[5];
	char rnge[11];
	float frq;
		if(0==m_sTmpParm.GroundingMode)strcpy(grnd,"单端");
		else if(m_sTmpParm.GroundingMode==1)strcpy(grnd,"差分");
		switch(m_sTmpParm.InputRange)
		{
		case 0: strcpy(rnge,"-10～10V ");break;
		case 1: strcpy(rnge,"-5～5 V ");break;
		case 2: strcpy(rnge,"-2.5～2.5V");break;
		case 3: strcpy(rnge," 0～10V");break;
		}
		switch(m_sTmpParm.Gains)
		{
		case 0: strcpy(gain,"×1");break;
		case 1: strcpy(gain,"×2");break;
		case 2: strcpy(gain,"×4");break;
		case 3: strcpy(gain,"×8");break;
		}
	frq=256000.0f/(float)m_uElpSmp;

	str.Format("当前参数：首通道%d,末通道%d,%s方式,输入范围%s,增益%s,采样频率%4.4f",
		m_sTmpParm.FirstChannel,m_sTmpParm.LastChannel+m_sTmpParm.FirstChannel,grnd,rnge,gain,frq);
	}

ext:
	OutText(str);

//	m_TextPosX=20;	m_TextPosY=40;

}

BOOL CArtDataView::InitializeTimer()
{
	m_TimerIDSmp=timeSetEvent(m_uElpSmp,m_wAccuracy,
		SampDataProc,(DWORD)this,TIME_PERIODIC);

	m_TimerIDDrw=timeSetEvent(m_uElpDrw,m_wAccuracy,
		DrawDataProc,(DWORD)this,TIME_PERIODIC);

	if(m_TimerIDDrw==0||m_TimerIDSmp==0)
	{
		MessageBox("不能定时！");return(FALSE);
	}
	else
	{return(TRUE);}
}

void CArtDataView::OnSmplStop()
{
	// TODO: Add your command handler code here
	CArtDataDoc* pDoc=GetDocument();
	CString str;
	
	if(m_bTimerSmp=TRUE)    //到了采样时间？
	{
		timeEndPeriod(m_wAccuracy);timeKillEvent(m_TimerIDSmp);m_bTimerSmp=FALSE;
		m_dwStopTimeUs=GetTickCount();
		m_fTime=m_dwStopTimeUs-m_dwStartTimeUs;
	}

	if(m_bTimerDrw=TRUE)    //到了绘图时间？
	{timeKillEvent(m_TimerIDDrw);m_bTimerDrw=FALSE;	}

	if(m_bADWorking==TRUE)
	{
		if(!USB5935_ReleaseDeviceAD(m_hDevice)){MessageBox("无法关闭AD设备");}
		else{m_bADWorking=FALSE;}
	}

	if(m_bDeviceWorking==TRUE)
	{
		if(!USB5935_ReleaseDevice(m_hDevice)){MessageBox("无法关闭设备");}
		else{m_bDeviceWorking=FALSE;}//	m_iStopTimes++;}


//		for(int chnl=m_sTmpParm.FirstChannel;chnl<=m_sTmpParm.FirstChannel+m_sTmpParm.LastChannel;chnl++)
		{
			//long seg=pDoc->m_iSegIndex[chnl];
			//pDoc->m_iCtlVct[chnl].push_back(seg);//通道chnl的段序
			//long t=(long)m_segStartTimeUs;
			//pDoc->m_iCtlVct.push_back((long)m_segStartTimeUs);//段开始时间               DWORD			long fstch=;

		pDoc->m_iCtlVct.push_back((long)pDoc->m_fDatVct[pDoc->m_iCtlVct[0]].size());//本段数据长度			long stpt=;
		pDoc->m_iCtlVct.push_back((long)(m_dwStopTimeUs-m_dwStartTimeUs));//时长

		}
		
			int stopT=pDoc->m_iCtlVct[7];
			int datCount=pDoc->m_iCtlVct[6];//(seg==0?pDoc->m_iCtlVct[chnl][10*seg+8]:pDoc->m_iCtlVct[chnl][10*seg+8]-pDoc->m_iCtlVct[chnl][10*seg-2]);
				//fstIndex=seg==0?0:pDoc->m_iCtlVct[chnl][10*seg-2];
			char grnd[6],rnge[12],gain[4];

			if(0==pDoc->m_iCtlVct[3]){strcpy(grnd,"单端");}
			else{strcpy(grnd,"差分");}

			switch(pDoc->m_iCtlVct[4])
			{
			case 0: strcpy(rnge,"-10～10V ");break;
			case 1: strcpy(rnge,"-5～5 V ");break;
			case 2: strcpy(rnge,"-2.5～2.5V");break;
			case 3: strcpy(rnge," 0～10V");break;
			}

			switch(pDoc->m_iCtlVct[2])
			{
			case 0: strcpy(gain,"×1");break;
			case 1: strcpy(gain,"×2");break;
			case 2: strcpy(gain,"×4");break;
			case 3: strcpy(gain,"×8");break;
			}

			//frq=256000.0f/(float)pDoc->m_iCtlVct[5];

			str.Format("本次采样时长%d (s),每通道得%d个数据",m_iSmplTime,datCount);
			OutText(str);
			str.Format("可以用Left/Right,Up/Dn,Ins/Del,Home/End,PgUp/PgDn键调整数据视图！");
			OutText(str);
			
	}

}


void CArtDataView::OnSmplReset() 
{
	// TODO: Add your command handler code here
	if(NULL!=m_hDevice)USB5935_ResetDevice(m_hDevice);
	
}

void CArtDataView::ReDrawData(UINT nChar)
{
/*		static float ampfT=1.0f,ampfV=1.0f;
		static int dt=0;
		BOOL KeyHit=FALSE;
	CArtDataDoc* pDoc=GetDocument();
	long totalTimeCap;

	if(pDoc->m_bFromFile||!m_bADWorking)  //&&m_iStopTimes!=0))
	{
					totalTimeCap=pDoc->m_iCtlVct[7];//采样时长

		switch(nChar)
		{
		case VK_LEFT:
			if(m_fTime-dt>m_iTotalDispTimeCapUs)m_fTime-=dt;
			KeyHit=TRUE;
			break;
		case VK_RIGHT:
			if(m_fTime+dt<totalTimeCap)m_fTime+=dt;
			KeyHit=TRUE;
			break;
		case VK_NEXT:
			if(m_fTime-m_iTotalDispTimeCapUs>m_iTotalDispTimeCapUs)m_fTime-=m_iTotalDispTimeCapUs;
			KeyHit=TRUE;
			break;
		case VK_PRIOR:
			if(m_fTime+m_iTotalDispTimeCapUs<totalTimeCap)m_fTime+=m_iTotalDispTimeCapUs;
			KeyHit=TRUE;
			break;
		case VK_HOME:
			m_fTime=totalTimeCap;
			KeyHit=TRUE;
			break;
		case VK_END:
			m_fTime=m_iTotalDispTimeCapUs;
			KeyHit=TRUE;
			break;
		case VK_UP:
			m_fAmplfV*=1.08f;
			KeyHit=TRUE;
			break;
		case VK_DOWN:
			if(m_fAmplfV>1)m_fAmplfV*=0.92f;
			else if(m_fAmplfV<1)m_fAmplfV=1.0f;
			KeyHit=TRUE;
			break;
		case VK_DELETE:
			if(m_iTotalDispTimeCapUs*0.92>m_uElpSmp)m_iTotalDispTimeCapUs*=0.92f;
			KeyHit=TRUE;
			break;
		case VK_INSERT:
			if(m_iTotalDispTimeCapUs*1.08<totalTimeCap)m_iTotalDispTimeCapUs*=1.08f;
			KeyHit=TRUE;
			break;
		}	
	}
	if(KeyHit)
	{
		pDoc->m_iDatPtr+=m_fTime;m_fTime=0;
	CArtDataDoc* pDoc = GetDocument();
	int PicWidth=650,PicHeigh=250,PicPosX=50,PicPosY=120;
	int OriginOfY=PicHeigh/2;
	CDC *pDC = GetDC();
	m_bByMembFun=TRUE;
	OnDraw(pDC);
*/				
/*		Invalidate();
		//创建一个内存中的显示设备
		CDC MemDC;	MemDC.CreateCompatibleDC(NULL);
		CBitmap MemBitmap;	MemBitmap.CreateCompatibleBitmap(pDC,PicWidth+200,PicHeigh);		//创建一个内存中的图像		
		MemDC.SelectObject(&MemBitmap); 		//指定内存显示设备在内存中的图像上画图
		CPen *pNewPen,*pOldPen;//定义各种类型的画笔
		MemDC.FillSolidRect(0,0,PicWidth+200,PicHeigh,RGB(20,20,20));//先用一种颜色作为内存显示设备的背景色		
		//MemDC.SetBkColor(RGB(2,2,250));

		static int iColorIndex[][3]={{255,128,128},{255,255,128},{128,255,128},{128,255,255},{0,128,255},
									{255,128,255},{0,128,128},{128,0,128},{64,64,128},{128,64,128},{128,0,0},
									{255,128,0},{255,128,255},{128,0,0},{128,64,64},{255,255,255}};
	//	static int iFirstChnl=m_sTmpParm.FirstChannel;
		static float InputRange[][2]={{-10,20},{-5,10},{-2.5,5},{0,10}};
		static float InpBotm=-10,//InputRange[m_sCdParm.InputRange][0],
			InpRang=20;//InputRange[m_sCdParm.InputRange][1];
*///////////////////////////////////////
/*
		CString strs,str;
		CFile file("Temp1.txt",CFile::modeCreate|CFile::modeWrite);
		CArchive arTxt(&file,CArchive::store);
		for(int chn=0;chn<16;chn++)
		{
			int s=pDoc->m_iCtlVct[chn].size();
			for(int i=0;i<s;i++)
			{
				str.Format("%d,   ",pDoc->m_iCtlVct[chn][i]);
				strs+=str;
			}
			strs+=";\n";
		}
		for(int k=0;k<strs.GetLength();k++)	{arTxt<<strs.GetAt(k);}
*/
/*		POINT GridPt[48],LegendPt[48];
		CString str;		
		m_iTotalDispTimeCapUs*=ampfT;ampfT=1.0f;
		for(int i=1;i<10;i++)
		{
			str.Format("%2.2f",i*((float)(m_iTotalDispTimeCapUs)/10000.0));
			pDC->TextOut(PicPosX+i*PicWidth/10-8,PicPosY+PicHeigh,str);
		}
		pDC->TextOut(PicPosX+i*PicWidth/10-16,PicPosY+PicHeigh,"s");
		for(i=1;i<8;i++)
		{
			str.Format("%1.1f",(i*InpRang/8+InpBotm)/ampfV);  //显示纵坐标标度
			pDC->TextOut(PicPosX-26,PicPosY+PicHeigh-i*PicHeigh/8-8,str);
		}
		pDC->TextOut(PicPosX-13,PicPosY+PicHeigh-i*PicHeigh/8,"V");
		int a=-1;////////////网格线的点
		for(i=0;i<18;i+=2)
		{
			a*=-1;
			GridPt[i].x=PicWidth/2-a*PicWidth/2;
			GridPt[i].y=i*PicHeigh/16;
			a*=-1;
			GridPt[i+1].x=PicWidth/2-a*PicWidth/2;
			GridPt[i+1].y=i*PicHeigh/16;
			a*=-1;
		}
		for(;i<=40;i+=2)
		{
			a*=-1;
			GridPt[i].y=PicHeigh/2-a*PicHeigh/2;
			GridPt[i].x=PicWidth-(i-18)*PicWidth/20;
			a*=-1;
			GridPt[i+1].y=PicHeigh/2-a*PicHeigh/2;
			GridPt[i+1].x=PicWidth-(i-18)*PicWidth/20;
			a*=-1;
		}
		for(int ch=0;ch<16;ch++)
		{
			LegendPt[3*ch].x=PicWidth+68;  LegendPt[3*ch].y=PicHeigh-240+ch*PicHeigh/17;
			LegendPt[3*ch+1].x=PicWidth+60;LegendPt[3*ch+1].y=PicHeigh-240+ch*PicHeigh/17;
			LegendPt[3*ch+2].x=PicWidth+60;LegendPt[3*ch+2].y=PicHeigh-240+(ch+1)*PicHeigh/17;
		}

		pNewPen=new CPen;
		pNewPen->CreatePen(PS_DOT,1,RGB(255,255,0));
		pOldPen=MemDC.SelectObject(pNewPen);
		MemDC.Polyline(GridPt,40);
		MemDC.Polyline(LegendPt,47);
		MemDC.SelectObject(pOldPen);
		delete pNewPen;
////////////////////////////////////////////
		//pDoc->m_iCtlVct[chnl]: 
		//0:SegN0;1:StartTime;2:FirstChannel;3:LastChannel;4:Gains;
		//5:GroundingMode;6:InputRange;7:m_uElpSmp;8:m_iDatIndex[chnl];9:StopTime
//////////////////////////////////////////
		int iDatIndex,chnl;
		float f;
		for(chnl=0;chnl<16;chnl++)
		{
			pNewPen=new CPen;
			int R=iColorIndex[chnl][0],G=iColorIndex[chnl][1],B=iColorIndex[chnl][2];
			pNewPen->CreatePen(PS_SOLID,1,RGB(R,G,B));
			pOldPen=MemDC.SelectObject(pNewPen);

			int segmnt;
			for(segmnt=0;segmnt<pDoc->m_iCtlVct[chnl].size()/10;segmnt++)
			{			 	
				float segStartTime=(float)pDoc->m_iCtlVct[chnl][10*segmnt+1];
				float segStopTime=(float)pDoc->m_iCtlVct[chnl][10*segmnt+9];

				if(segStopTime>m_fTime-m_iTotalDispTimeCapUs&&segStartTime<=m_fTime)
				{
				float segDatT=segStopTime-segStartTime;
				float segDatC;
				if(segmnt==0)segDatC=(float)pDoc->m_iCtlVct[chnl][10*segmnt+8];
				else if(segmnt>0) segDatC=(float)(pDoc->m_iCtlVct[chnl][10*segmnt+8]-pDoc->m_iCtlVct[chnl][10*segmnt-2]);
				float seguElpSmp=(float)pDoc->m_iCtlVct[chnl][segmnt*10+7];
				int iTotalDispCount=(int)(256.0/seguElpSmp*m_iTotalDispTimeCapUs);
				float fVctSmpCor=(float)iTotalDispCount/(float)PicWidth;
				if(fVctSmpCor<1){dt=1;} else dt=fVctSmpCor;

					if(m_fTime<=(float)pDoc->m_iCtlVct[chnl][10*segmnt+9]&&m_fTime>=(float)pDoc->m_iCtlVct[chnl][10*segmnt+1])
					{InpBotm=InputRange[pDoc->m_iCtlVct[chnl][10*segmnt+6]][0];
					InpRang=InputRange[pDoc->m_iCtlVct[chnl][10*segmnt+6]][1];}
					float EndDispTime=segStartTime>m_fTime-m_iTotalDispTimeCapUs?segStartTime:m_fTime-m_iTotalDispTimeCapUs;
					float BegnDispTime=segStopTime>m_fTime?m_fTime:segStopTime;
					float VoidDatC=(m_fTime-segStopTime)*256.0/seguElpSmp;
					int yOffset,xOffset;
					if(segStopTime>m_fTime)
					{
						yOffset=-(int)VoidDatC;
						xOffset=0;
					}
					else
					{
						yOffset=0;
						xOffset=(int)(VoidDatC/fVctSmpCor);
					}
					float DispDatC=(BegnDispTime-EndDispTime)*256.0/seguElpSmp;

					POINT DatPt[650]={0};					
					for(f=0.0,i=0;f<DispDatC;f+=fVctSmpCor,i++)
					{
						DatPt[i].x=xOffset+i;
						iDatIndex=pDoc->m_iCtlVct[chnl][10*segmnt+8]-1-yOffset-(int)f;
						if(iDatIndex>=pDoc->m_fDatVct[chnl].size()-1){iDatIndex=pDoc->m_fDatVct[chnl].size()-1;}
						else if(iDatIndex<0){iDatIndex=0;}
						DatPt[i].y=PicHeigh-PicHeigh*(ampfV*pDoc->m_fDatVct[chnl][iDatIndex]-InpBotm)/InpRang;
					}
					MemDC.Polyline(DatPt,i);

					POINT DatPtIn[]={{PicWidth+10,PicHeigh-240+(chnl)*PicHeigh/17},
												{PicWidth+50,PicHeigh-240+(chnl)*PicHeigh/17}};
					MemDC.Polyline(DatPtIn,2);////////画图例
				}
			}//for(segmnt=0;...
			MemDC.SelectObject(pOldPen);
			delete pNewPen;
		}//for(chnl=0;...)
 			pDC->BitBlt(PicPosX,PicPosY,PicWidth+200,PicHeigh+20, &MemDC, 0, 0, SRCCOPY);
			ReleaseDC(pDC);		

	}//if(KeyHit)*/
}

void CArtDataView::OnKeyDown(UINT nChar, UINT nRepCnt, UINT nFlags) 
{
	// TODO: Add your message handler code here and/or call default
		static float ampfT=1.0f,ampfV=1.0f;
		BOOL KeyHit=FALSE;
	CArtDataDoc* pDoc=GetDocument();//

	if(pDoc->m_bFromFile||!m_bADWorking)  //&&m_iStopTimes!=0))
	{

		int PicWidth=650;

		int iTotalDispCount=(int)(256.0/(float)m_uElpSmp*m_iTotalDispTimeCapUs);// 窗口时长所包含的通道数据点数
		float fVctSmpCor=(float)iTotalDispCount/(float)PicWidth;//数据到窗口的映射系数
			CClientDC dc(this);
			CString str;

		switch(nChar)
		{
		case VK_LEFT:
			if(0!=pDoc->m_iCtlVct.size())
			{
				if((pDoc->m_iDatPtr-1>=iTotalDispCount)&&(iTotalDispCount<pDoc->m_iCtlVct[6])) 
				pDoc->m_iDatPtr-=1;
			}
			KeyHit=TRUE;
			//str.Format("p=%d, c=%f, s=%d",pDoc->m_iDatPtr,fVctSmpCor,pDoc->m_iCtlVct.size());dc.TextOut(10,10,str);
			break;
		case VK_RIGHT:
			if(0!=pDoc->m_iCtlVct.size())
			{
				if((pDoc->m_iDatPtr+1<pDoc->m_iCtlVct[6])&&(iTotalDispCount<pDoc->m_iCtlVct[6])) 
				pDoc->m_iDatPtr+=1;
			}
			KeyHit=TRUE;
			//str.Format("p=%d, c=%f,s=%d",pDoc->m_iDatPtr,fVctSmpCor,pDoc->m_iCtlVct.size());dc.TextOut(10,10,str);
			break;
		case VK_NEXT:
			if(0!=pDoc->m_iCtlVct.size())
			{
				if((pDoc->m_iDatPtr+iTotalDispCount<=pDoc->m_iCtlVct[6])&&(iTotalDispCount<pDoc->m_iCtlVct[6])) 
				pDoc->m_iDatPtr+=iTotalDispCount;
			}
			KeyHit=TRUE;
			break;
		case VK_PRIOR:
			if((pDoc->m_iDatPtr-iTotalDispCount>=iTotalDispCount)&&(iTotalDispCount<pDoc->m_iCtlVct[6])) 
				pDoc->m_iDatPtr-=iTotalDispCount;
			KeyHit=TRUE;
			break;
		case VK_HOME:
			pDoc->m_iDatPtr=(pDoc->m_iCtlVct.size()?iTotalDispCount:0);
			KeyHit=TRUE;
			break;
		case VK_END:
			pDoc->m_iDatPtr=(pDoc->m_iCtlVct.size()?pDoc->m_iCtlVct[6]-1:0);
			KeyHit=TRUE;
			break;
		case VK_UP:
			m_fAmplfV*=1.08f;
			KeyHit=TRUE;
			break;
		case VK_DOWN:
			if(m_fAmplfV>1)m_fAmplfV*=0.92f;
			else if(m_fAmplfV<1)m_fAmplfV=1.0f;
			KeyHit=TRUE;
			break;
		case VK_DELETE:
			if(m_iTotalDispTimeCapUs*0.92>m_uElpDrw) m_iTotalDispTimeCapUs*=0.92f;
			KeyHit=TRUE;
			break;
		case VK_INSERT:
			if(m_iTotalDispTimeCapUs*1.08<(pDoc->m_iCtlVct.size()?pDoc->m_iCtlVct[7]:m_iSmplTime*1000))
				m_iTotalDispTimeCapUs*=1.08f;
			KeyHit=TRUE;
			break;
		}	
	}

	if(KeyHit)
	{
		CArtDataDoc* pDoc = GetDocument();

		CDC *pDC = GetDC();
		m_bByMembFun=TRUE;
		OnDraw(pDC);
	}
				
	CScrollView::OnKeyDown(nChar, nRepCnt, nFlags);
}

void CArtDataView::OnClear() 
{
	// TODO: Add your command handler code here
	CArtDataDoc* pDoc=GetDocument();
	for(int chnl=0;chnl<19;chnl++)
	{
		pDoc->m_fDatVct[chnl].clear();
//		m_fDatVct[i].resize(0);
		//pDoc->m_iSegIndex[chnl]=0;
	}
//	m_dwStartTimeUs=GetTickCount();
	pDoc->m_iCtlVct.clear();
	pDoc->m_bSaved=FALSE;
}

void CArtDataView::OnDestroy() 
{
	CScrollView::OnDestroy();
	
	// TODO: Add your message handler code here
	OnSmplStop();OnClear();
}

void CArtDataView::OutText(CString str)
{
	m_sOutText[0]=m_sOutText[1];
	m_sOutText[1]=m_sOutText[2];
	m_sOutText[2]=m_sOutText[3];
	m_sOutText[3]=m_sOutText[4];
	m_sOutText[4]=str;
}

void CArtDataView::OnMove(int x, int y) 
{
	CScrollView::OnMove(x, y);
	
	// TODO: Add your message handler code here
//	CString a="";
//	DrawData();
//	OutText(a);
}

void CArtDataView::DrawAnal()
{
	CArtDataDoc* pDoc=GetDocument();

	double realMax=0.0f,realMin=0.0f,imgMax=0.0f,imgMin=0.0f;			
	double temp=0.0f;
	int i,j;
	int PicPosX=50,PicPosY=0;
	int PicWidth=720,PicHeigh=250;////PicWidth=650,PicHeigh=250,PicPosX=50,PicPosY=120;

	POINT DatPt[720]={0};
	CString str;
	m_cAnalDC.FillSolidRect(0,0,992,2900,RGB(116,255,108));//背景色
		CPen *pOldPen,*pNewPen=new CPen;
		pNewPen->CreatePen(PS_SOLID,1,RGB(255,0,0));
		pOldPen=m_cAnalDC.SelectObject(pNewPen);


	if(0==pDoc->m_iAnalCtl[0]||3==pDoc->m_iAnalCtl[0]||6==pDoc->m_iAnalCtl[0]||7==pDoc->m_iAnalCtl[0])
	{
		realMax=pDoc->m_fDatVct[17][0];
		realMin=pDoc->m_fDatVct[17][0];
		for(i=1;i<pDoc->m_fDatVct[17].size();i++)
		{
			if(realMax<pDoc->m_fDatVct[17][i]){realMax=pDoc->m_fDatVct[17][i];}
			if(realMin>pDoc->m_fDatVct[17][i]){realMin=pDoc->m_fDatVct[17][i];}
		}

		float dt=(pDoc->m_fDatVct[16][1]-pDoc->m_fDatVct[16][0])/((float)PicWidth-1.0f); //横坐标刻度
		float dx=pDoc->m_fDatVct[17].size()/(float)PicWidth;
		for(i=0;i<PicWidth;i++)
		{
			DatPt[i].x=i+PicPosX;
			temp=pDoc->m_fDatVct[17][(int)(i*dx)];
			for(j=0;j<dx;j++)
			{
				if(abs(temp)<abs(pDoc->m_fDatVct[17][(int)(i*dx)+j])){temp=pDoc->m_fDatVct[17][(int)(i*dx)+j];}
			}
			DatPt[i].y=PicHeigh-(temp-realMin)*PicHeigh/(realMax-realMin);
		}

		m_cAnalDC.Rectangle(PicPosX,PicPosY,PicWidth+PicPosX,PicHeigh+PicPosY);

		m_cAnalDC.Polyline(DatPt,PicWidth);
		
		str.Format("%1.2e",realMax);m_cAnalDC.TextOut(PicPosX+PicWidth,PicPosY,str);
		str.Format("%1.2e",realMin);m_cAnalDC.TextOut(PicPosX+PicWidth,PicPosY+PicHeigh-20,str);

		str.Format("%1.2e",pDoc->m_fDatVct[16][0]);m_cAnalDC.TextOut(PicPosX,PicPosY+PicHeigh,str);
		str.Format("%1.2e (ms)",pDoc->m_fDatVct[16][1]);m_cAnalDC.TextOut(PicPosX+PicWidth-20,PicPosY+PicHeigh,str);

		char antyp[36];
		switch(pDoc->m_iAnalCtl[0])
		{
		case 0: strcpy(antyp,"卷     积");break;
		case 3: strcpy(antyp,"反 卷 积");break;
		case 6: strcpy(antyp,"误差  函数");break;
		case 7: strcpy(antyp,"余误差函数");break;
		}
		m_cAnalDC.TextOut(PicPosX+PicWidth/2-30,PicPosY+PicHeigh,antyp);
	}


//////////////////////////////////////////
	if(4==pDoc->m_iAnalCtl[0]||5==pDoc->m_iAnalCtl[0])
	{
		realMax=pDoc->m_fDatVct[17][0];////////绘制实频曲线
		realMin=pDoc->m_fDatVct[17][0];
		for(i=0;i<pDoc->m_fDatVct[17].size();i++)
		{
			if(realMax<pDoc->m_fDatVct[17][i]){realMax=pDoc->m_fDatVct[17][i];}
			if(realMin>pDoc->m_fDatVct[17][i]){realMin=pDoc->m_fDatVct[17][i];}
		}

		float dt=(pDoc->m_fDatVct[16][1]-pDoc->m_fDatVct[16][0])/((float)PicWidth-1.0f);

		float dx=pDoc->m_fDatVct[17].size()/(float)PicWidth;

		for(i=0;i<PicWidth;i++)
		{
			DatPt[i].x=i+PicPosX;
			temp=pDoc->m_fDatVct[17][(int)(i*dx)];
			for(j=0;j<dx;j++)
			{
				if(abs(temp)<abs(pDoc->m_fDatVct[17][(int)(i*dx+j)])){temp=pDoc->m_fDatVct[17][(int)(i*dx+j)];}
			}
			DatPt[i].y=PicHeigh-(temp-realMin)*PicHeigh/(realMax-realMin);
		}
		m_cAnalDC.Rectangle(PicPosX,PicPosY,PicPosX+PicWidth,PicPosY+PicHeigh);

		m_cAnalDC.Polyline(DatPt,PicWidth);

		str.Format("%1.2e",realMax);m_cAnalDC.TextOut(PicPosX+PicWidth,PicPosY,str);
		str.Format("%1.2e",realMin);m_cAnalDC.TextOut(PicPosX+PicWidth,PicPosY+PicHeigh-20,str);

		str.Format("%1.2e",pDoc->m_fDatVct[16][0]);m_cAnalDC.TextOut(PicPosX,PicPosY+PicHeigh,str);
		str.Format("%1.2e (Hz)",pDoc->m_fDatVct[16][1]);m_cAnalDC.TextOut(PicPosX+PicWidth-20,PicPosY+PicHeigh,str);

		m_cAnalDC.TextOut(PicPosX+PicWidth/2,PicPosY+PicHeigh,"实-频");

		///////////////////////////////////绘制虚频曲线////////////////////
		PicPosY=1.1*PicHeigh;

		imgMax=pDoc->m_fDatVct[18][0];
		imgMin=pDoc->m_fDatVct[18][0];
		for(i=0;i<pDoc->m_fDatVct[18].size();i++)
		{
			if(imgMax<pDoc->m_fDatVct[18][i]){imgMax=pDoc->m_fDatVct[18][i];}
			if(imgMin>pDoc->m_fDatVct[18][i]){imgMin=pDoc->m_fDatVct[18][i];}
		}

		for(i=0;i<PicWidth;i++)//////////////
		{
			temp=pDoc->m_fDatVct[18][(int)(i*dx)];
			for(j=0;j<dx;j++)
			{
				if(abs(temp)<abs(pDoc->m_fDatVct[18][(int)(i*dx)+j])){temp=pDoc->m_fDatVct[18][(int)(i*dx)+j];}
			}
			DatPt[i].y=PicPosY+PicHeigh-(temp-imgMin)*PicHeigh/(imgMax-imgMin);
		}

		m_cAnalDC.Rectangle(PicPosX,PicPosY,PicWidth+PicPosX,PicHeigh+PicPosY);

		m_cAnalDC.Polyline(DatPt,PicWidth);

		str.Format("%1.2e",imgMax);m_cAnalDC.TextOut(PicPosX+PicWidth,PicPosY,str);
		str.Format("%1.2e",imgMin);m_cAnalDC.TextOut(PicPosX+PicWidth,PicPosY+PicHeigh-20,str);
		

		str.Format("%1.2e",pDoc->m_fDatVct[16][0]);m_cAnalDC.TextOut(PicPosX,PicPosY+PicHeigh,str);
		str.Format("%1.2e (Hz)",pDoc->m_fDatVct[16][1]);m_cAnalDC.TextOut(PicPosX+PicWidth-20,PicPosY+PicHeigh,str);

		m_cAnalDC.TextOut(PicPosX+PicWidth/2,PicPosY+PicHeigh,"虚-频");
		/////////////////////////////////////////////
		//////////////绘制模频曲线
		PicPosY=2.2*PicHeigh;

		double normMax=sqrt(pDoc->m_fDatVct[17][0]*pDoc->m_fDatVct[17][0]+pDoc->m_fDatVct[18][0]*pDoc->m_fDatVct[18][0]);
		double normMin=sqrt(pDoc->m_fDatVct[17][0]*pDoc->m_fDatVct[17][0]+pDoc->m_fDatVct[18][0]*pDoc->m_fDatVct[18][0]);
		double *normM=new double[pDoc->m_fDatVct[17].size()];
		for(i=0;i<pDoc->m_fDatVct[17].size();i++)
		{
			normM[i]=sqrt(pDoc->m_fDatVct[17][i]*pDoc->m_fDatVct[17][i]+pDoc->m_fDatVct[18][i]*pDoc->m_fDatVct[18][i]);
			if(normMax<normM[i]){normMax=normM[i];}
			if(normMin>normM[i]){normMin=normM[i];}
		}

		for(i=0;i<PicWidth;i++)
		{
			temp=normM[i];
			for(j=0;j<dx;j++)
			{
				if(abs(temp)<abs(normM[(int)(i*dx)+j])){temp=normM[(int)(i*dx)+j];}
			}
			DatPt[i].y=PicPosY+PicHeigh-(temp-normMin)*PicHeigh/(normMax-normMin);
		}

		m_cAnalDC.Rectangle(PicPosX,PicPosY,PicWidth+PicPosX,PicHeigh+PicPosY);

		m_cAnalDC.Polyline(DatPt,PicWidth);		
		delete normM;

		str.Format("%1.2e",normMax);m_cAnalDC.TextOut(PicPosX+PicWidth,PicPosY,str);
		str.Format("%1.2e",normMin);m_cAnalDC.TextOut(PicPosX+PicWidth,PicPosY+PicHeigh-20,str);
		
		str.Format("%1.2e",pDoc->m_fDatVct[16][0]);m_cAnalDC.TextOut(PicPosX,PicPosY+PicHeigh,str);
		str.Format("%1.2e (Hz)",pDoc->m_fDatVct[16][1]);m_cAnalDC.TextOut(PicPosX+PicWidth-20,PicPosY+PicHeigh,str);

		m_cAnalDC.TextOut(PicPosX+PicWidth/2,PicPosY+PicHeigh,"幅值谱");

		///////////////////////////////////////////////
		PicPosY=3.3*PicHeigh;

		double phaseMax=pDoc->m_fDatVct[17][0]?atan(pDoc->m_fDatVct[18][0]/pDoc->m_fDatVct[17][0]):3.1415926/2;
		double phaseMin=phaseMax;
		double *phaseM=new double[pDoc->m_fDatVct[17].size()];
		for(i=0;i<pDoc->m_fDatVct[17].size();i++)
		{
			phaseM[i]=pDoc->m_fDatVct[17][i]?atan(pDoc->m_fDatVct[18][i]/pDoc->m_fDatVct[17][i]):3.1415926;
			if(phaseMax<phaseM[i]){phaseMax=phaseM[i];}
			if(phaseMin>phaseM[i]){phaseMin=phaseM[i];}
		}

		for(i=0;i<PicWidth;i++)
		{
			temp=phaseM[i];
			for(j=0;j<dx;j++)
			{
				if(abs(temp)<abs(phaseM[(int)(i*dx)+j])){temp=phaseM[(int)(i*dx)+j];}
			}
			DatPt[i].y=PicPosY+PicHeigh-(temp-normMin)*PicHeigh/(normMax-normMin);
		}
		m_cAnalDC.Rectangle(PicPosX,PicPosY,PicWidth+PicPosX,PicHeigh+PicPosY);

		m_cAnalDC.Polyline(DatPt,PicWidth);
		delete phaseM;

		str.Format("%1.2e",phaseMax);m_cAnalDC.TextOut(PicPosX+PicWidth,PicPosY,str);
		str.Format("%1.2e",phaseMin);m_cAnalDC.TextOut(PicPosX+PicWidth,PicPosY+PicHeigh-20,str);

		str.Format("%1.2e",pDoc->m_fDatVct[16][0]);m_cAnalDC.TextOut(PicPosX,PicPosY+PicHeigh,str);
		str.Format("%1.2e (Hz)",pDoc->m_fDatVct[16][1]);m_cAnalDC.TextOut(PicPosX+PicWidth-20,PicPosY+PicHeigh,str);

		m_cAnalDC.TextOut(PicPosX+PicWidth/2,PicPosY+PicHeigh,"相位谱");

	}///if(4==pDoc->m_iAnalCtl[0]......
	delete pNewPen;
}
