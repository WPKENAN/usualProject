// ArtDataView.h : interface of the CArtDataView class
//
/////////////////////////////////////////////////////////////////////////////

#if !defined(AFX_ARTDATAVIEW_H__44FD4E1E_9877_46CD_9E0E_5ACE57A2B831__INCLUDED_)
#define AFX_ARTDATAVIEW_H__44FD4E1E_9877_46CD_9E0E_5ACE57A2B831__INCLUDED_

#include "CardDlg.h"	// Added by ClassView
#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

#include "ArtDataDoc.h"
#include "MainFrm.h"

class CArtDataView : public CScrollView
{
protected: // create from serialization only
	CArtDataView();
	DECLARE_DYNCREATE(CArtDataView)

// Attributes
public:
	CArtDataDoc* GetDocument();
	BOOL m_bCurvDisp;
	BOOL m_bDeviceWorking,m_bADWorking;//标识数据是否用曲线显示；设备是否正在工作
	BOOL m_bTimerSmp;
	BOOL m_bTimerDrw;
	BOOL m_bSmpFlag;
	BOOL m_bDrwFlag;
//	BOOL m_bFirstSmp;
	BOOL m_bByMembFun;
	BOOL m_bEnableOutText;

	CCardDlg *m_pCdDlg;                               //指向参数设置对话框
    USB5935_PARA_AD	m_sCdParm,m_sTmpParm;        //初始化采集卡结构体
	int m_iSmplFrq;                              //保存参数对话框频率选项
	int m_iChAmount[2];                          //单端和差分情况下的通道数
	HANDLE m_hDevice;                            //设备句柄
	USHORT m_nADBuffer[4096];                    //读AD缓冲区
	LONG m_nRetSizeWords;                        //一次AD读得的数据个数
	LONG m_nReadSizeWords;                       //一次AD要读的数据个数
	unsigned int m_iSmplTime;                   //保存参数对话框的时长选项
	DWORD m_dwStartTimeUs,m_dwStopTimeUs;//,m_segStartTimeUs;
	UINT m_uElpSmp,m_uElpDrw;                    //采样周期、绘图周期：毫秒
	UINT m_TimerIDSmp,m_TimerIDDrw;
	UINT m_wAccuracy;
	//UINT m_iStartTimes,m_iStopTimes;
	float m_fAmplfV;//, m_fAmplfT;纵坐标在显示窗口的放大倍数
	CString m_sOutText[5];

	CDC m_cAnalDC;
;

//	int m_TextPosX,m_TextPosY;

//	CAnalDlg m_cAnDlg;

// Operations
public:
// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CArtDataView)
	public:
	virtual void OnDraw(CDC* pDC);  // overridden to draw this view
	virtual BOOL PreCreateWindow(CREATESTRUCT& cs);
	protected:
	virtual void OnInitialUpdate(); // called first time after construct
	//}}AFX_VIRTUAL

// Implementation
public:
	void DrawAnal();
	void OutText(CString);
	float m_fTime;
	float m_iTotalDispTimeCapUs;
	BOOL m_bNewSmpParm;
//	void FFT(double* data,int n,BOOL isInverse=FALSE);
	BOOL InitializeTimer();
	void ReadCard();
	void DrawData();
	void ReDrawData(UINT nChar);
	virtual ~CArtDataView();
#ifdef _DEBUG
	virtual void AssertValid() const;
	virtual void Dump(CDumpContext& dc) const;
#endif

protected:

// Generated message map functions
protected:
	//{{AFX_MSG(CArtDataView)
	afx_msg void OnSmplParm();
	afx_msg void OnSmplDisplay();
	afx_msg void OnSmplStart();
	afx_msg void OnSmplStop();
	afx_msg void OnTimer(UINT nIDEvent);
	afx_msg void OnSmplReset();
	afx_msg void OnKeyDown(UINT nChar, UINT nRepCnt, UINT nFlags);
	afx_msg void OnClear();
	afx_msg void OnDestroy();
	afx_msg void OnMove(int x, int y);
	afx_msg void OnVScroll(UINT nSBCode, UINT nPos, CScrollBar* pScrollBar);
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
private:
	CSize m_clientSize;
};

#ifndef _DEBUG  // debug version in ArtDataView.cpp
inline CArtDataDoc* CArtDataView::GetDocument()
   { return (CArtDataDoc*)m_pDocument; }
#endif

/////////////////////////////////////////////////////////////////////////////

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_ARTDATAVIEW_H__44FD4E1E_9877_46CD_9E0E_5ACE57A2B831__INCLUDED_)
