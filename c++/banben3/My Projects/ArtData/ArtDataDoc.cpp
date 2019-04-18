#include "stdafx.h"
#include "ArtData.h"
#include "Usb5935.h"
#include "ArtDataDoc.h"
#include "MainFrm.h"
#include "ClrDatDlg.h"
#include "ArtDataView.h"
#include "shlwapi.h"
// ArtDataDoc.cpp : implementation of the CArtDataDoc class
//


#ifdef _DEBUG
#define new DEBUG_NEW
#undef THIS_FILE
static char THIS_FILE[] = __FILE__;
#endif

/////////////////////////////////////////////////////////////////////////////
// CArtDataDoc

IMPLEMENT_DYNCREATE(CArtDataDoc, CDocument)

BEGIN_MESSAGE_MAP(CArtDataDoc, CDocument)
	//{{AFX_MSG_MAP(CArtDataDoc)
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CArtDataDoc construction/destruction

CArtDataDoc::CArtDataDoc()
{
	// TODO: add one-time construction code here
	vector<float> lineF;
	lineF.clear();
	for(int i=0;i<19;i++)
	{
		m_fDatVct.push_back(lineF);
		m_iCtlVct.push_back(0);
	}
	m_iCtlVct.clear();
	m_iDatPtr=0;

	for(i=0;i<3;i++)m_iAnalCtl[i]=0;

	m_bFromFile=FALSE;
	m_bSaved=FALSE;

	m_strPathName="1234.txt";
}

CArtDataDoc::~CArtDataDoc()
{
	for(int i=0;i<16;i++)
	{
		m_fDatVct[i].clear();
//		m_fDatVct[i].resize(0);
		m_iCtlVct.clear();
	}
	m_fDatVct.clear();
//	m_fDatVct.resize(0);
	m_iCtlVct.clear();
}

BOOL CArtDataDoc::OnNewDocument()
{
	if (!CDocument::OnNewDocument())
		return FALSE;

	// TODO: add reinitialization code here
	// (SDI documents will reuse this document)
	
	return TRUE;
}



/////////////////////////////////////////////////////////////////////////////
// CArtDataDoc serialization

void CArtDataDoc::Serialize(CArchive& ar)
{
	CMainFrame* pMainFrame=(CMainFrame*)AfxGetMainWnd();
	CArtDataView* pView=(CArtDataView*)pMainFrame->GetActiveView();
//	CClientDC dc(pView);

	CFile* pFile=ar.GetFile();
	CString strFile=pFile->GetFileTitle();
/*//	dc.TextOut(0,0,strFile);

	CDocTemplate* pTemplate = GetDocTemplate();
	CString newName,strExt,str;

	if (pTemplate->GetDocString(strExt, CDocTemplate::filterExt) &&  !strExt.IsEmpty())
	{
		ASSERT(strExt[0] == '.');
		newName += strExt;
	}
//	if(newName!="art"){m_bSaveAsTXT=TRUE;}
//	else{m_bSaveAsTXT=FALSE;}
*/
	if (ar.IsStoring())
	{
		// TODO: add storing code here
			char grnd[5];
			char rnge[11];
			char gain[4];
			long stopT;
			long datCount;

			int chnl,fstch,lstch;

/*			char drive[_MAX_DRIVE]; 
			char dir[_MAX_DIR]; 
			char fname[_MAX_FNAME]; 
			char ext[_MAX_EXT]; 

			CFile file("Temp.txt",CFile::modeCreate|CFile::modeWrite);
			CArchive arTxt(&file,CArchive::store);

			for(fstch=0;fstch<16;fstch++)
			{
				if(m_iSegIndex[fstch]!=0)
				{seg=0;break;}
			}

			for(lstch=15;lstch>=0;lstch--)
			{
				if(m_iSegIndex[lstch]!=0)
				{seg=0;break;}
			}

			chnl=fstch;
*/
			CString str,strs="\n\t###������ѧArtData����ϵͳ1.0�棬2013��  ��Ȩ���У���е����ѧԺ����ʵ����###\n ";

			stopT=m_iCtlVct[7];
			datCount=m_iCtlVct[6];

			if(0==m_iCtlVct[3])strcpy(grnd,"����");
			else strcpy(grnd,"���");

			switch(m_iCtlVct[4])
			{
			case 0: strcpy(rnge,"-10��10V ");break;
			case 1: strcpy(rnge,"-5��5 V ");break;
			case 2: strcpy(rnge,"-2.5��2.5V");break;
			case 3: strcpy(rnge," 0��10V");break;
			}

			switch(m_iCtlVct[2])
			{
			case 0: strcpy(gain,"��1");break;
			case 1: strcpy(gain,"��2");break;
			case 2: strcpy(gain,"��4");break;
			case 3: strcpy(gain,"��8");break;
			}

			fstch=m_iCtlVct[0];
			lstch=m_iCtlVct[1];

			str.Format("[���ݸ�����ʱ��%d ms,%s�ӵ�,��ѹ%s,����%s,��������%d ms,����ͨ������%d,ĩ%d,ÿͨ����%d������]\n\n",
						 stopT,grnd,rnge,gain,m_iCtlVct[5],fstch,lstch,datCount);
			strs+=str;

			for(chnl=fstch;chnl<=lstch;chnl++)
			{
				str.Format("\tͨ��%2.2d=\n",chnl);
				strs+=str;

				for(int i=0;i<datCount;i++)
				{
					str.Format("%f,",m_fDatVct[chnl][i]);
					strs+=str;
				}
				str.Format("%f",m_fDatVct[chnl][i]);
				strs+=str;
				strs+=";\n";
			}
			for(int k=0;k<strs.GetLength();k++)
			{ar<<strs.GetAt(k);}
		
	}
////////////////////////////////////////////////////////////////////////////////////////
	else
	{
		// TODO: add loading code here
		char c='#';
		int chnl;
		long uTime=0,ampf,fstch,lstch,datcount;
		long InpRng,Gain,rng,grnd;
		long uElpSmp;
		CString strHeader,strDat;
		BOOL DocIsEmpty=1;

		if(m_iCtlVct.size()) DocIsEmpty=0;

		if(!DocIsEmpty)
		{
			CClrDatDlg clrdatDlg;
			CString s;
			int ch;

			switch(clrdatDlg.DoModal())
			{
			case IDOK:
				for(ch=0;ch<19;ch++)
				{
					m_fDatVct[ch].clear();
				}
				m_iCtlVct.clear();
				//	m_iSegIndex[ch]=0;
				s.Format("ͨ�������������");
				pView->OutText(s);
				pView->m_dwStartTimeUs=0;
				m_bSaved=FALSE;
				break;
			case IDCANCEL:
				s.Format("���ȱ���ͨ�����ݣ�");
				pView->OutText(s);
				goto ext;
			}
		}

		else
		{
			for(int i=0;i<280&&c!=']';i++)
			{
				ar>>c;strHeader+=c;
			}

			//for(i=0;i<strHeader.GetLength();i++)
			{
				int posc;
				posc=strHeader.Find("��");
				if(-1!=posc)
				{
					uTime=atoi(strHeader.Mid(posc+2,10));
				}
				else
				{
					pView->MessageBox("�ļ���ʽ��:�޷���ȡ����ʱ����");
					goto ext;
				}

				posc=strHeader.Find("��");
				if(-1!=posc)
				{
					grnd=(strHeader.Mid(posc-4,4)=="���"?1:0);
				}
				else
				{
					pView->MessageBox("�ļ���ʽ���޷���ȡ�ӵط�ʽ��");
					goto ext;
				}

				posc=strHeader.Find("ѹ");
				if(-1!=posc)
				{
					rng=atoi(strHeader.Mid(posc+2,4));
					switch(rng)
					{
					case -10: InpRng=0;break;
					case -5:  InpRng=1;break;
					case -2:  InpRng=2;break;
					case 0:   InpRng=3;
					}
				}
				else
				{
					pView->MessageBox("�ļ���ʽ���޷���ȡ��ѹ��Χ��");
					goto ext;
				}

				posc=strHeader.Find("��");
				if(-1!=posc)
				{
					ampf=atoi(strHeader.Mid(posc+2,4));
					switch(ampf)
					{
					case 1: Gain=0;break;
					case 2: Gain=1;break;
					case 4: Gain=2;break;
					case 8: Gain=3;break;
					}
				}
				else
				{
					pView->MessageBox("�ļ���ʽ���޷���ȡ���棡");
					goto ext;
				}

				posc=strHeader.Find("��");
				if(-1!=posc)
				{
					char ff[15];
					strcpy(ff,strHeader.Mid(posc+2,15));
					uElpSmp=atoi(ff);
				}
				else
				{
					pView->MessageBox("�ļ���ʽ���޷���ȡ�������ڣ�");
					goto ext;
				}

				posc=strHeader.Find("��");
				if(-1!=posc)
				{
					fstch=atoi(strHeader.Mid(posc+2,4));
				}
				else
				{
					pView->MessageBox("�ļ���ʽ���޷���ȡ��ͨ����");
					goto ext;
				}

				posc=strHeader.Find("ĩ");
				if(-1!=posc)
				{
					lstch=atoi(strHeader.Mid(posc+2,4));
				}
				else
				{
					pView->MessageBox("�ļ���ʽ���޷���ȡĩͨ����");
					goto ext;
				}
				
				posc=strHeader.Find("��");
				if(-1!=posc)
				{
					datcount=atoi(strHeader.Mid(posc+2,11));
				}
				else
				{
					pView->MessageBox("�ļ���ʽ���޷���ȡ���ݳ��ȣ�");
					goto ext;
				}
			}

			m_iCtlVct.clear();
			for(chnl=fstch;chnl<=lstch;chnl++)
			{
				m_iCtlVct.push_back((long)fstch);//���ε���ͨ����LONG			long lstch=;
				m_iCtlVct.push_back((long)lstch);//ĩͨ����LONG			long gn=;
				m_iCtlVct.push_back((long)Gain);//���ε�����       LONG			long grnd=;
				m_iCtlVct.push_back((long)grnd);//���νӵ� LONG			long inprg=;
				m_iCtlVct.push_back((long)InpRng);//���������ѹ��Χ           LONG: 0~3			long elp=;
				m_iCtlVct.push_back((long)uElpSmp);//���β�������             UINT			long siz=;
				m_iCtlVct.push_back((long)datcount);//�������ݳ���			long stpt=;
				m_iCtlVct.push_back((long)uTime);//ʱ��
			}

			for(chnl=fstch;chnl<=lstch;chnl++)
			{
				for(i=0;(c!='=')&&(i<12);i++){ar>>c;}  //Ѱ���ļ���ͨ�����ݵĿ�ʼ'='

				CString strDat;//ar>>a;CString s;
				for(;(c!=';');){ar>>c;strDat+=c;}//��'='�������ͨ���������ַ�����strDat

				int start=0;
				CString a;
				for(int count=0;count<datcount;count++)
				{
					//char a[12];
					//strcpy(a,strDat.Mid(start+1,12));
					a=strDat.Mid(start+1,12);
					m_fDatVct[chnl].push_back(atof(a));
					start=strDat.Find(',',start+1);
				}
				strDat.Empty();
				
				m_iDatPtr=m_fDatVct[chnl].size()-1;

			}

			m_bSaved=TRUE;m_bFromFile=TRUE;
		}

ext:	;//





/*			CFile file2("Temp2.txt",CFile::modeCreate|CFile::modeWrite);
			CArchive arT2(&file2,CArchive::store);
			CString str,strs;
			int chnl,i;
		for(chnl=0;chnl<16;chnl++)
		{m_fDatVct[chnl].clear();m_iCtlVct[chnl].clear();}

//		vector<long> lineL;		vector<float> lineF;

		for(chnl=0;chnl<16;chnl++)
		{
			ar>>m_iSegIndex[chnl];
		}
		for(chnl=0;chnl<16;chnl++)
		{
			long a;
			for(i=0;i<10*m_iSegIndex[chnl];i++)
			{
				ar>>a;
				m_iCtlVct[chnl].push_back(a);
			}
		}

		for(i=0;i<strs.GetLength();i++)
		{arT2<<strs.GetAt(i);}
		for(chnl=0;chnl<16;chnl++)
		{
			if(m_iCtlVct[chnl].size()>0)
			{
				long chDatsiz=m_iCtlVct[chnl].size()-2;
				float b;
				for(int i=0;i<m_iCtlVct[chnl][chDatsiz];i++)
				{
					ar>>b;
					m_fDatVct[chnl].push_back(b);
				}
			}
		}
*/	
	/*
	CMainFrame* pMainFrame=(CMainFrame*)AfxGetMainWnd();
	CArtDataView* pView=(CArtDataView*)pMainFrame->GetActiveView();
	pView->Invalidate();*/
		
	}

}

/////////////////////////////////////////////////////////////////////////////
// CArtDataDoc diagnostics

#ifdef _DEBUG
void CArtDataDoc::AssertValid() const
{
	CDocument::AssertValid();
}

void CArtDataDoc::Dump(CDumpContext& dc) const
{
	CDocument::Dump(dc);
}
#endif //_DEBUG

/////////////////////////////////////////////////////////////////////////////
// CArtDataDoc commands
/*
void CArtDataDoc::OnFileSave() 
{
	// TODO: Add your command handler code here
//	Serialize(CArchive& ar);
}

void CArtDataDoc::OnFileSave() 
{
	// TODO: Add your command handler code here
	
}
*/
