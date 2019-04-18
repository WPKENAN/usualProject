// ArtData.h : main header file for the ARTDATA application
//

#if !defined(AFX_ARTDATA_H__8949627F_73CB_4401_8481_3ECD47C12D18__INCLUDED_)
#define AFX_ARTDATA_H__8949627F_73CB_4401_8481_3ECD47C12D18__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

#ifndef __AFXWIN_H__
	#error include 'stdafx.h' before including this file for PCH
#endif

#include "resource.h"       // main symbols

/////////////////////////////////////////////////////////////////////////////
// CArtDataApp:
// See ArtData.cpp for the implementation of this class
//

class CArtDataApp : public CWinApp
{
public:
	CArtDataApp();

// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CArtDataApp)
	public:
	virtual BOOL InitInstance();
	//}}AFX_VIRTUAL

// Implementation
	//{{AFX_MSG(CArtDataApp)
	afx_msg void OnAppAbout();
		// NOTE - the ClassWizard will add and remove member functions here.
		//    DO NOT EDIT what you see in these blocks of generated code !
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};


/////////////////////////////////////////////////////////////////////////////

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_ARTDATA_H__8949627F_73CB_4401_8481_3ECD47C12D18__INCLUDED_)
