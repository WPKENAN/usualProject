#ifndef _USB5935_DEVICE_
#define _USB5935_DEVICE_

#include<windows.h>
//***********************************************************
// ����AD�ɼ��Ĳ����ṹ
typedef struct _USB5935_PARA_AD
{
	LONG FirstChannel;      // ��ͨ��,ȡֵ��ΧΪ[0, 15]
	LONG LastChannel;		// ĩͨ��,ȡֵ��ΧΪ[0, 15]
	LONG GroundingMode;		// �ӵط�ʽ�����˻�˫��ѡ��
	LONG InputRange;		// ģ�����������̷�Χ
	LONG Gains;				// ����
} USB5935_PARA_AD, *PUSB5935_PARA_AD;

//***********************************************************
// AD����(USB5935_PARA_AD)�е�GroundingModeʹ�õ�ģ���źŽӵط�ʽѡ��
const long USB5935_GNDMODE_SE			= 0x00;	// ���˷�ʽ(SE:Single end)
const long USB5935_GNDMODE_DI			= 0x01;	// ˫�˷�ʽ(DI:Differential)

//***********************************************************
// ADӲ������USB5935_PARA_AD�е�InputRangeģ�������뷶Χ��ʹ�õ�ѡ��
const long USB5935_INPUT_N10000_P10000mV= 0x00; // ��10000mV
const long USB5935_INPUT_N5000_P5000mV	= 0x01; // ��5000mV
const long USB5935_INPUT_N2500_P2500mV	= 0x02; // ��2500mV
const long USB5935_INPUT_0_P10000mV		= 0x03; // 0��10000mV

//***********************************************************
// ADӲ������USB5935_PARA_AD�е�ADGainsʹ�õ�Ӳ������ѡ��
#define USB5935_1MULT_GAINS		0x00	// 1������(ʹ��PGA202��PGA203�Ŵ���)
#define USB5935_2MULT_GAINS		0x01	// 2������(ʹ��PGA202�Ŵ���)
#define USB5935_4MULT_GAINS		0x02	// 4������(ʹ��PGA202�Ŵ���)
#define USB5935_8MULT_GAINS		0x03	// 8������(ʹ��PGA202�Ŵ���)

//***********************************************************
// ���ڼ������Ĳ����ṹ
typedef struct _USB5935_PARA_CNT
{
	LONG FunctionMode;		// ����ģʽ, 0:������ģʽCOUNTER, 1:���巢����ģʽ
	LONG ClockSource;		// ʱ��Դѡ��
	LONG GateMode;			// �ſ�ģʽ
	LONG bEnableBuffer;		// �������ʹ��, 0: ��ֹ���������1: ���������
	LONG OutputDir;			// ���������ƽ����
	LONG bCoutinue;			// ������Ƿ��������
	LONG OutputType;		// ��ʱ�����巢����ʽ����Ч������������͡�
} USB5935_PARA_CNT, *PUSB5935_PARA_CNT;

//***********************************************************
// Ӳ������USB5935_PARA_CNT�е�FunctionMode����ģʽѡ��
const long USB5935_FUNCMODE_COUNTER		= 0x00;	// ������ģʽ
const long USB5935_FUNCMODE_TIMER		= 0x01;	// ���嶨ʱ������ģʽ

//***********************************************************
// Ӳ������USB5935_PARA_CNT�е�ClockSource����ģʽѡ��
const long USB5935_CLOCKSRC_LOCAL_CLK	= 0x00;	// �忨�ֲ���Ƶʱ��(��40M�����Ƶ����,��SetLocalCLKFreq�趨)
const long USB5935_CLOCKSRC_CLOCK_IN	= 0x01;	// �ⲿʱ���ź�Դ����(SOURCE)

//***********************************************************
// Ӳ������USB5935_PARA_CNT�е�GateMode���ſ�ģʽѡ��
const long USB5935_GATEMODE_UNUSE_0		= 0x00;		// COUNTER:��ʹ���ſ��ź�(�����ڼ��¼�����)
													// TIMER:��ʹ��GATE�ĵ������巢��(�����ڵ������巢����)
const long USB5935_GATEMODE_RISING_1	= 0x01;		// COUNTER:GATE�ϱ��ش�������������������Ч
													// TIMER:GATE�ϱ��ص��δ������巢��(�����ڵ��δ��������巢����)
const long USB5935_GATEMODE_FALLING_2	= 0x02;		// COUNTER:GATE�±��ش���,����������Ч
													// TIMER:GATE�±��ص��δ������巢��(�����ڵ��δ��������巢����)
const long USB5935_GATEMODE_POSITIVE_3	= 0x03;		// COUNTER:�ߵ�ƽ��Ч(�������ſ��¼�����)
													// TIMER:GATE�ϱ����ظ��������巢��(�������ظ����������巢����)
const long USB5935_GATEMODE_NEGATIVE_4	= 0x04;		// COUNTER:�͵�ƽ��Ч(�������ſ��¼�����)
													// TIMER:GATE�±����ظ��������巢��(�������ظ����������巢����)
const long USB5935_GATEMODE_RSTART_FSTOP_5	= 0x05;	// COUNTER:�ϱ��ش����������±���ֹͣ����(�����ڵ������Ȳ���)
													// TIMER:GATE�ϱ��ص��δ����������崮������
const long USB5935_GATEMODE_FSTART_RSTOP_6	= 0x06;	// COUNTER:�±��ش����������ϱ���ֹͣ����(�����ڵ������Ȳ���)
													// TIMER:GATE�±��ص��δ����������崮������
const long USB5935_GATEMODE_PSTART_PSTOP_7	= 0x07;	// COUNTER:�ϱ��ش�����������һ���ϱ���ֹͣ����(�����ڵ����ڲ���)
													// TIMER:GATE�ߵ�ƽ�����������崮������
const long USB5935_GATEMODE_NSTART_NSTOP_8	= 0x08;	// COUNTER:�±��ش�����������һ���±���ֹͣ����(�����ڵ����ڲ���)
													// TIMER:GATE�͵�ƽ�����������崮������

// Ӳ������USB5935_PARA_CNT�е�OutputDir���������ѡ��
const long USB5935_OUTPUTDIR_NEGATIVE		= 0x00;	// ��ֹ��������£�����͵�ƽ��Ч
const long USB5935_OUTPUTDIR_POSITIVE		= 0x01;	// ��ֹ��������£�����ߵ�ƽ��Ч

// Ӳ������USB5935_PARA_CNT�е�OutputType���������ѡ��
const long USB5935_OUTPUTTYPE_TOGGLE		= 0x00;	// ռ�ձȿ��趨���η�ʽ(����InitValue��WidthValue���������ڶ�ʱ�����巢����ʽ�����ò���ռ�ձ�)
const long USB5935_OUTPUTTYPE_PULSE			= 0x01;	// ���巽ʽ

//***********************************************************
// CreateFileObject�е�Mode����ʹ�õ��ļ�������ʽ������(��ͨ����ָ��ʵ�ֶ��ַ�ʽ������)
const long	USB5935_modeRead			= 0x0000;   // ֻ���ļ���ʽ
const long  USB5935_modeWrite			= 0x0001;   // ֻд�ļ���ʽ
const long 	USB5935_modeReadWrite		= 0x0002;   // �ȶ���д�ļ���ʽ
const long  USB5935_modeCreate			= 0x1000;   // ����ļ�������Դ������ļ���������ڣ����ؽ����ļ�������0

//***********************************************************
// ���������ӿ�
#ifndef _USB5935_DRIVER_
#define DEVAPI __declspec(dllimport)
#else
#define DEVAPI __declspec(dllexport)
#endif

#ifdef __cplusplus
extern "C" {
#endif
	//######################## ����ͨ�ú��� #################################
	HANDLE DEVAPI FAR PASCAL USB5935_CreateDevice(int DeviceLgcID = 0); // �����豸����(�ú���ʹ��ϵͳ���߼��豸ID��
	HANDLE DEVAPI FAR PASCAL USB5935_CreateDeviceEx(int DevicePhysID = 0); // �����豸����(�ú���ʹ�ð忨�����豸ID��
	int DEVAPI FAR PASCAL USB5935_GetDeviceCount(HANDLE hDevice);      // ȡ��USB5935��ϵͳ�е��豸����
	BOOL DEVAPI FAR PASCAL USB5935_GetDeviceCurrentID(HANDLE hDevice, PLONG DeviceLgcID, PLONG DevicePhysID); // ȡ�õ�ǰ�豸���߼�ID�ź�����ID��
	BOOL DEVAPI FAR PASCAL USB5935_ListDeviceDlg(void); // �öԻ����б�ϵͳ���е�����USB5935�豸
	BOOL DEVAPI FAR PASCAL USB5935_ResetDevice(HANDLE hDevice);		 // ��λ����USB�豸
    BOOL DEVAPI FAR PASCAL USB5935_ReleaseDevice(HANDLE hDevice);    // �ͷ��豸

	//####################### AD���ݶ�ȡ���� #################################
    BOOL DEVAPI FAR PASCAL USB5935_InitDeviceAD(				// ��ʼ���豸,������TRUE��,�豸���̿�ʼ����.
									HANDLE hDevice,				// �豸���,��Ӧ��CreateDevice��������
									PUSB5935_PARA_AD pADPara);  // Ӳ������, �����ڴ˺����о���Ӳ��״̬							

    BOOL DEVAPI FAR PASCAL USB5935_ReadDeviceAD(				// ��ʼ���豸�󣬼����ô˺�����ȡ�豸�ϵ�AD����
									HANDLE hDevice,				// �豸���,��Ӧ��CreateDevice��������
									USHORT ADBuffer[],			// �����ڽ������ݵ��û�������
									LONG nReadSizeWords,		// ��ȡAD���ݵĳ���(��)  
									PLONG nRetSizeWords = NULL);// ʵ�ʷ������ݵĳ���(��)

    BOOL DEVAPI FAR PASCAL USB5935_ReleaseDeviceAD(HANDLE hDevice); // ֹͣAD�ɼ����ͷ�AD������ռ��Դ

   	//################# AD��Ӳ�������������� ########################	
	BOOL DEVAPI FAR PASCAL USB5935_SaveParaAD(HANDLE hDevice, PUSB5935_PARA_AD pADPara);  
    BOOL DEVAPI FAR PASCAL USB5935_LoadParaAD(HANDLE hDevice, PUSB5935_PARA_AD pADPara);
    BOOL DEVAPI FAR PASCAL USB5935_ResetParaAD(HANDLE hDevice, PUSB5935_PARA_AD pADPara); // ��AD���������ָ�������Ĭ��ֵ

	//##################### ���������ƺ��� ##########################
    BOOL DEVAPI FAR PASCAL USB5935_InitDeviceCNT(				// ��ʼ��������
									HANDLE hDevice,				// �豸���
									PUSB5935_PARA_CNT pCNTPara); // ������������

	ULONG DEVAPI FAR PASCAL USB5935_SetLCLKFreqCNT(			// ���ñ���ʱ��Ƶ��(LCLK=Local Clock),����ʵ�ʵķ�Ƶ��
									HANDLE hDevice,			// �豸������,����CreateDevice��������
									double Frequency);		// ʱ��Ƶ��ֵ

	BOOL DEVAPI FAR PASCAL USB5935_SetDeviceCNT(			// ���ü������ĳ�ֵ
									HANDLE hDevice,			// �豸������,����CreateDevice��������
									ULONG CNTVal,			// ������ֵ, COUNTER: ������ֵ��TIMER:��ʱ��ʼ������(246λ)
									ULONG WidthVal);		// ��ȳ�ֵ, COUNTER: ��Ч�� TIMER:���������(24λ)

	BOOL DEVAPI FAR PASCAL USB5935_GetDeviceCNT(			// ȡ�ø�·�������ĵ�ǰ����ֵ
									HANDLE hDevice,			// �豸������,����CreateDevice��������
									PULONG pCNTVal,			// ���ؼ���ֵ
									PULONG pWidthVal);		// ���ؿ��ֵ

	BOOL DEVAPI FAR PASCAL USB5935_GetDevStatusCNT(			// ��ü�����״̬
									HANDLE hDevice,			// �豸������,����CreateDevice��������
									PBOOL bOverflow,		// ��õļ����������־, =TRUE:��ʾ�����������, =FALSE:��ʾδ���
									PBOOL bBufferRefresh,	// ��õļ�����������±�־, =TRUE:��ʾ�����ѱ�����, =FALSE:��ʾδ����
									PBOOL bBufferLost);		// ��õļ��������嶪ʧ��־, =TRUE:��ʾ�����ѱ���ʧ, =FALSE:��ʾδ��ʧ

	BOOL DEVAPI FAR PASCAL USB5935_ClrDevStatusCNT(			// ���������״̬
									HANDLE hDevice,			// �豸������,����CreateDevice��������
									BOOL bClrOverflow,		// �Ƿ���������������־, =TRUE:��ʾ���, =FALSE:��ʾ�����
									BOOL bClrBufferRefresh,	// �Ƿ����������������±�־, =TRUE:��ʾ���, =FALSE:��ʾ�����
									BOOL bClrBufferLost);	// �Ƿ�������������嶪ʧ��־, =TRUE:��ʾ���, =FALSE:��ʾ�����

	BOOL DEVAPI FAR PASCAL USB5935_ReleaseDeviceCNT(		// �ͷź�ֹͣ����/��ʱ��
									HANDLE hDevice);		// �豸������,����CreateDevice��������

	//####################### ����I/O����������� #################################
	BOOL DEVAPI FAR PASCAL USB5935_GetDeviceDI(					// ȡ�ÿ�����״̬     
									HANDLE hDevice,				// �豸���,��Ӧ��CreateDevice��������								        
									BYTE bDISts[6]);			// ��������״̬(ע��: ���붨��Ϊ8���ֽ�Ԫ�ص�����)

    BOOL DEVAPI FAR PASCAL USB5935_SetDeviceDO(					// ���������״̬
									HANDLE hDevice,				// �豸���,��Ӧ��CreateDevice��������								        
									BYTE bDOSts[6]);			// �������״̬(ע��: ���붨��Ϊ8���ֽ�Ԫ�ص�����)

	//############################################################################
	BOOL DEVAPI FAR PASCAL USB5935_GetDevVersion(				// ��ȡ�豸�̼�������汾
									HANDLE hDevice,				// �豸������,����CreateDevice��������
									PULONG pulFmwVersion,		// �̼��汾
									PULONG pulDriverVersion);	// �����汾

   	//########################## �ļ��������� ####################################
    HANDLE DEVAPI FAR PASCAL USB5935_CreateFileObject(			// �����ļ�����
									HANDLE hDevice,				// �豸���,��Ӧ��CreateDevice��������
									LPCTSTR strFileName,		// ·�����ļ���
									int Mode);					// �ļ�������ʽ

    BOOL DEVAPI FAR PASCAL USB5935_WriteFile(					// �����û��ռ������ݵ������ļ�
									HANDLE hFileObject,			// �ļ����,��Ӧ��CreateFileObject��������
									PVOID pDataBuffer,			// �û����ݿռ��ַ
									LONG nWriteSizeBytes);		// ��������С(�ֽ�)

    BOOL DEVAPI FAR PASCAL USB5935_ReadFile(					// �Ӵ����ļ��ж�ȡ���ݵ��û��ռ�
									HANDLE hFileObject,			// �ļ����,��Ӧ��CreateFileObject��������
									PVOID pDataBuffer,			// �����ļ����ݵ��û��ڴ滺����
									LONG OffsetBytes,			// ���ļ�ǰ�˿�ʼ��ƫ��λ��
									LONG nReadSizeBytes);		// ��ƫ��λ�ÿ�ʼ�����ֽ���

	BOOL DEVAPI FAR PASCAL USB5935_SetFileOffset(				// �����ļ�ƫ��ָ��
									HANDLE hFileObject,			// �ļ����,��Ӧ��CreateFileObject��������
									LONG nOffsetBytes);			// �ļ�ƫ��λ�ã�����Ϊ��λ��  

	ULONGLONG DEVAPI FAR PASCAL USB5935_GetFileLength(HANDLE hFileObject); // ȡ��ָ���ļ����ȣ��ֽڣ�

    BOOL DEVAPI FAR PASCAL USB5935_ReleaseFile(HANDLE hFileObject);
    LONGLONG DEVAPI FAR PASCAL USB5935_GetDiskFreeBytes(		// ���ָ���̷��Ĵ��̿ռ�(ע��ʹ��64λ����)
								   LPCTSTR strDiskName);		// �̷���,��C��Ϊ"C:\\", D��Ϊ"D:\\"

	//############################ �̲߳������� ################################
	HANDLE DEVAPI FAR PASCAL USB5935_CreateSystemEvent(void); 	// �����ں�ϵͳ�¼�����
	BOOL DEVAPI FAR PASCAL USB5935_ReleaseSystemEvent(HANDLE hEvent); // �ͷ��ں��¼�����
	BOOL DEVAPI FAR PASCAL USB5935_CreateVBThread(HANDLE* hThread, LPTHREAD_START_ROUTINE RoutineAddr);
	BOOL DEVAPI FAR PASCAL USB5935_TerminateVBThread(HANDLE hThread);

	//################# �������Ӻ��� ########################
	BOOL DEVAPI FAR PASCAL USB5935_kbhit(void); // ̽���û��Ƿ��л�������(�ڿ���̨Ӧ�ó���Console�����ڷ�VC������)
	char DEVAPI FAR PASCAL USB5935_getch(void); // �ȴ�����ȡ�û�����ֵ(�ڿ���̨Ӧ�ó���Console����Ч)

#ifdef __cplusplus
}
#endif

//#################### �������� #####################

const long USB5935_MAX_AD_CHANNELS = 16;

#ifndef _USB5935_FIFO_LENGTH_
#define _USB5935_FIFO_LENGTH_
// ��������֧�ֵĸ���FIFO�洢���ĳ���(��)
const long FIFO_IDT7202_LENGTH				= 1024;
const long FIFO_IDT7203_LENGTH				= 2048;
const long FIFO_IDT7204_LENGTH				= 4096;
const long FIFO_IDT7205_LENGTH				= 8192;
const long FIFO_IDT7206_LENGTH				= 16384;
const long FIFO_IDT7207_LENGTH				= 32768;
#endif; // _USB5935_FIFO_LENGTH_

// �Զ������������������
#ifndef _USB5935_DRIVER_
#ifndef _WIN64
#pragma comment(lib, "USB5935_32.lib")
#pragma message("======== Welcome to use our art company's products!")
#pragma message("======== Automatically linking with USB5935_32.dll...")
#pragma message("======== Successfully linked with USB5935_32.dll")
#else
#pragma comment(lib, "USB5935_64.lib")
#pragma message("======== Welcome to use our art company's products!")
#pragma message("======== Automatically linking with USB5935_64.dll...")
#pragma message("======== Successfully linked with USB5935_64.dll")
#endif
#endif

#endif; // _USB5935_DEVICE_