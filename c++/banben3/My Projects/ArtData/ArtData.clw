; CLW file contains information for the MFC ClassWizard

[General Info]
Version=1
LastClass=CMainFrame
LastTemplate=CDialog
NewFileInclude1=#include "stdafx.h"
NewFileInclude2=#include "ArtData.h"
LastPage=0

ClassCount=10
Class1=CArtDataApp
Class2=CArtDataDoc
Class3=CArtDataView
Class4=CMainFrame

ResourceCount=21
Resource1=IDD_DIALOG1
Resource2=IDD_ANALYSIS2
Class5=CAboutDlg
Class6=CCardDlg
Resource3=IDD_NEWFILE_SAVE (English (U.S.))
Resource4=IDD_DATA_SAVE
Class7=CAnalDlg
Resource5=IDD_ABOUTBOX
Resource6=IDR_TOOLBAR1
Resource7=IDD_CARDDLG
Class8=CAnalDlg2
Resource8=IDR_MAINFRAME1
Resource9=IDR_MAINFRAME
Class9=CDatSavDlg
Resource10=IDD_ANALYSIS
Class10=CClrDatDlg
Resource11=IDD_CLRDAT
Resource12=145
Resource13=147
Resource14=152
Resource15=151
Resource16=128
Resource17=100
Resource18=130
Resource19=133
Resource20=136
Resource21=102 (English (U.S.))

[CLS:CArtDataApp]
Type=0
HeaderFile=ArtData.h
ImplementationFile=ArtData.cpp
Filter=N
LastObject=IDC_USETEMP

[CLS:CArtDataDoc]
Type=0
HeaderFile=ArtDataDoc.h
ImplementationFile=ArtDataDoc.cpp
Filter=N
BaseClass=CDocument
VirtualFilter=DC
LastObject=CArtDataDoc

[CLS:CArtDataView]
Type=0
HeaderFile=ArtDataView.h
ImplementationFile=ArtDataView.cpp
Filter=C
BaseClass=CScrollView
VirtualFilter=VWC
LastObject=CArtDataView


[CLS:CMainFrame]
Type=0
HeaderFile=MainFrm.h
ImplementationFile=MainFrm.cpp
Filter=T
LastObject=IDM_ANALSYS_GEN
BaseClass=CFrameWnd
VirtualFilter=fWC




[CLS:CAboutDlg]
Type=0
HeaderFile=ArtData.cpp
ImplementationFile=ArtData.cpp
Filter=D
LastObject=CAboutDlg
BaseClass=CDialog
VirtualFilter=dWC

[DLG:IDD_ABOUTBOX]
Type=1
Class=CAboutDlg
ControlCount=6
Control1=IDC_STATIC,static,1342308480
Control2=IDC_STATIC,static,1342308352
Control3=IDOK,button,1342373889
Control4=IDC_STATIC,static,1342308352
Control5=IDC_STATIC,static,1342308352
Control6=IDC_IMAGE2,{4C599241-6926-101B-9992-00000B65C6F9},1342177280

[MNU:IDR_MAINFRAME]
Type=1
Class=CMainFrame
Command1=ID_FILE_NEW
Command2=ID_FILE_OPEN
Command3=ID_FILE_SAVE
Command4=ID_FILE_SAVE_AS
Command5=ID_FILE_MRU_FILE1
Command6=ID_APP_EXIT
Command7=IDM_SMPL_PARM
Command8=IDM_SMPL_DISPLAY
Command9=IDM_SMPL_START
Command10=IDM_SMPL_STOP
Command11=IDM_SMPL_RESET
Command12=IDM_CLEAR
Command13=IDM_ANALSYS_GEN
Command14=IDM_ANALYSIS_REL
Command15=ID_VIEW_TOOLBAR
Command16=ID_VIEW_STATUS_BAR
Command17=ID_HELP_FINDER
Command18=ID_APP_ABOUT
CommandCount=18

[ACL:IDR_MAINFRAME]
Type=1
Class=CMainFrame
Command1=ID_EDIT_COPY
Command2=ID_FILE_NEW
Command3=ID_FILE_OPEN
Command4=ID_FILE_SAVE
Command5=ID_EDIT_PASTE
Command6=ID_EDIT_UNDO
Command7=ID_EDIT_CUT
Command8=ID_HELP
Command9=ID_CONTEXT_HELP
Command10=ID_NEXT_PANE
Command11=ID_PREV_PANE
Command12=ID_EDIT_COPY
Command13=ID_EDIT_PASTE
Command14=ID_KEY_CTLLEFT
Command15=ID_CTLLEFT
Command16=ID_CTLLEFT
Command17=ID_EDIT_CUT
Command18=ID_EDIT_UNDO
CommandCount=18

[CLS:CCardDlg]
Type=0
HeaderFile=CardDlg.h
ImplementationFile=CardDlg.cpp
BaseClass=CDialog
Filter=D
LastObject=CCardDlg
VirtualFilter=dWC

[DLG:IDD_CARDDLG]
Type=1
Class=CCardDlg
ControlCount=17
Control1=IDOK,button,1342242817
Control2=IDCANCEL,button,1342242816
Control3=IDC_STATIC,button,1342177287
Control4=IDC_STATIC,button,1342177287
Control5=IDC_STATIC,button,1342177287
Control6=IDC_STATIC,button,1342177287
Control7=IDC_STATIC,button,1342177287
Control8=IDC_STATIC,button,1342177287
Control9=IDC_STATIC,button,1342177287
Control10=IDC_SIGNL_GAIN,combobox,1344339970
Control11=IDC_SIGNL_GRND,combobox,1344339970
Control12=IDC_SIGNL_RNG,combobox,1344339970
Control13=IDC_FST_CHNNL,combobox,1344339970
Control14=IDC_LST_CHNNL,combobox,1344339970
Control15=IDC_SMPL_FRQ,combobox,1344339970
Control16=IDC_SMPL_TIME,edit,1350643840
Control17=IDC_STATIC,static,1342308352

[DLG:IDD_ANALYSIS]
Type=1
Class=?
ControlCount=11
Control1=IDOK,button,1342242817
Control2=IDCANCEL,button,1342242816
Control3=IDC_COMBO1,combobox,1344340226
Control4=IDC_COMBO2,combobox,1344340226
Control5=IDC_STATIC,button,1342177287
Control6=IDC_STATIC,static,1342308352
Control7=IDC_STATIC,static,1342308352
Control8=IDC_STATIC,button,1342177287
Control9=IDC_LIST2,SysListView32,1350631424
Control10=IDC_BUTTON1,button,1342242816
Control11=IDC_COMBO3,combobox,1344340226

[DLG:IDD_DIALOG1]
Type=1
Class=CAnalDlg
ControlCount=3
Control1=IDOK,button,1342242817
Control2=IDCANCEL,button,1342242816
Control3=IDC_STATIC,static,1342308352

[CLS:CAnalDlg]
Type=0
HeaderFile=AnalDlg.h
ImplementationFile=AnalDlg.cpp
BaseClass=CDialog
Filter=D
LastObject=CAnalDlg
VirtualFilter=dWC

[TB:IDR_TOOLBAR1]
Type=1
Class=?
Command1=IDM_SMPL_PARM
Command2=IDM_SMPL_START
Command3=IDM_SMPL_STOP
Command4=IDM_ANALSYS_GEN
Command5=ID_APP_ABOUT
CommandCount=5

[TB:IDR_MAINFRAME1]
Type=1
Class=?
Command1=ID_FILE_NEW
Command2=ID_FILE_OPEN
Command3=ID_FILE_SAVE
Command4=IDM_SMPL_PARM
Command5=IDM_SMPL_START
Command6=IDM_SMPL_STOP
Command7=IDM_SMPL_DISPLAY
Command8=ID_APP_ABOUT
Command9=ID_CONTEXT_HELP
CommandCount=9

[DLG:IDD_ANALYSIS2]
Type=1
Class=CAnalDlg2
ControlCount=7
Control1=IDOK,button,1342242817
Control2=IDCANCEL,button,1342242816
Control3=IDC_DATASEG,edit,1350631552
Control4=IDC_ANALTYPE,combobox,1344339970
Control5=IDC_STATIC,button,1342177287
Control6=IDC_STATIC,button,1342177287
Control7=IDC_DATASEG2,edit,1350631552

[CLS:CAnalDlg2]
Type=0
HeaderFile=AnalDlg2.h
ImplementationFile=AnalDlg2.cpp
BaseClass=CDialog
Filter=D
LastObject=CAnalDlg2
VirtualFilter=dWC

[DLG:IDD_NEWFILE_SAVE (English (U.S.))]
Type=1
Class=?
ControlCount=1
Control1=IDC_STATIC,static,1342308352

[DLG:IDD_DATA_SAVE]
Type=1
Class=CDatSavDlg
ControlCount=4
Control1=IDOK,button,1342242817
Control2=IDCANCEL,button,1342242816
Control3=IDC_STATIC,static,1342308352
Control4=IDNO,button,1342242817

[CLS:CDatSavDlg]
Type=0
HeaderFile=DatSavDlg.h
ImplementationFile=DatSavDlg.cpp
BaseClass=CDialog
Filter=D
LastObject=CDatSavDlg

[DLG:IDD_CLRDAT]
Type=1
Class=CClrDatDlg
ControlCount=3
Control1=IDOK,button,1342242817
Control2=IDCANCEL,button,1342242816
Control3=IDC_STATIC,static,1342308352

[CLS:CClrDatDlg]
Type=0
HeaderFile=ClrDatDlg.h
ImplementationFile=ClrDatDlg.cpp
BaseClass=CDialog
Filter=D
LastObject=CClrDatDlg

[TB:128]
Type=1
Class=?
CommandCount=0

[TB:145]
Type=1
Class=?
CommandCount=0

[MNU:128]
Type=1
Class=?
CommandCount=0

[ACL:128]
Type=1
Class=?
CommandCount=0

[DLG:100]
Type=1
Class=?
ControlCount=6
Control1=65535,static,1342308480
Control2=65535,static,1342308352
Control3=1,button,1342373889
Control4=65535,static,1342308352
Control5=65535,static,1342308352
Control6=1024,{4C599241-6926-101B-9992-00000B65C6F9},1342177280

[DLG:130]
Type=1
Class=?
ControlCount=17
Control1=1,button,1342242817
Control2=2,button,1342242816
Control3=65535,button,1342177287
Control4=65535,button,1342177287
Control5=65535,button,1342177287
Control6=65535,button,1342177287
Control7=65535,button,1342177287
Control8=65535,button,1342177287
Control9=65535,button,1342177287
Control10=1000,combobox,1344339970
Control11=1001,combobox,1344339970
Control12=1002,combobox,1344339970
Control13=1008,combobox,1344339970
Control14=1009,combobox,1344339970
Control15=1011,combobox,1344339970
Control16=1007,edit,1350643840
Control17=65535,static,1342308352

[DLG:133]
Type=1
Class=?
ControlCount=11
Control1=1,button,1342242817
Control2=2,button,1342242816
Control3=1005,combobox,1344340226
Control4=1006,combobox,1344340226
Control5=65535,button,1342177287
Control6=65535,static,1342308352
Control7=65535,static,1342308352
Control8=65535,button,1342177287
Control9=1016,SysListView32,1350631424
Control10=1017,button,1342242816
Control11=1010,combobox,1344340226

[DLG:136]
Type=1
Class=?
ControlCount=3
Control1=1,button,1342242817
Control2=2,button,1342242816
Control3=65535,static,1342308352

[DLG:147]
Type=1
Class=?
ControlCount=7
Control1=1,button,1342242817
Control2=2,button,1342242816
Control3=1030,edit,1350631552
Control4=1031,combobox,1344339970
Control5=65535,button,1342177287
Control6=65535,button,1342177287
Control7=1032,edit,1350631552

[DLG:151]
Type=1
Class=?
ControlCount=4
Control1=1,button,1342242817
Control2=2,button,1342242816
Control3=65535,static,1342308352
Control4=7,button,1342242817

[DLG:152]
Type=1
Class=?
ControlCount=3
Control1=1,button,1342242817
Control2=2,button,1342242816
Control3=65535,static,1342308352

[DLG:102 (English (U.S.))]
Type=1
Class=?
ControlCount=1
Control1=65535,static,1342308352

