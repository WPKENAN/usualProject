#ifndef _USB5935_DEVICE_
#define _USB5935_DEVICE_

#include<windows.h>
//***********************************************************
// 用于AD采集的参数结构
typedef struct _USB5935_PARA_AD
{
	LONG FirstChannel;      // 首通道,取值范围为[0, 15]
	LONG LastChannel;		// 末通道,取值范围为[0, 15]
	LONG GroundingMode;		// 接地方式（单端或双端选择）
	LONG InputRange;		// 模拟量输入量程范围
	LONG Gains;				// 增益
} USB5935_PARA_AD, *PUSB5935_PARA_AD;

//***********************************************************
// AD参数(USB5935_PARA_AD)中的GroundingMode使用的模拟信号接地方式选项
const long USB5935_GNDMODE_SE			= 0x00;	// 单端方式(SE:Single end)
const long USB5935_GNDMODE_DI			= 0x01;	// 双端方式(DI:Differential)

//***********************************************************
// AD硬件参数USB5935_PARA_AD中的InputRange模拟量输入范围所使用的选项
const long USB5935_INPUT_N10000_P10000mV= 0x00; // ±10000mV
const long USB5935_INPUT_N5000_P5000mV	= 0x01; // ±5000mV
const long USB5935_INPUT_N2500_P2500mV	= 0x02; // ±2500mV
const long USB5935_INPUT_0_P10000mV		= 0x03; // 0～10000mV

//***********************************************************
// AD硬件参数USB5935_PARA_AD中的ADGains使用的硬件增益选项
#define USB5935_1MULT_GAINS		0x00	// 1倍增益(使用PGA202或PGA203放大器)
#define USB5935_2MULT_GAINS		0x01	// 2倍增益(使用PGA202放大器)
#define USB5935_4MULT_GAINS		0x02	// 4倍增益(使用PGA202放大器)
#define USB5935_8MULT_GAINS		0x03	// 8倍增益(使用PGA202放大器)

//***********************************************************
// 用于计数器的参数结构
typedef struct _USB5935_PARA_CNT
{
	LONG FunctionMode;		// 功能模式, 0:计数器模式COUNTER, 1:脉冲发生器模式
	LONG ClockSource;		// 时钟源选择
	LONG GateMode;			// 门控模式
	LONG bEnableBuffer;		// 缓冲计数使能, 0: 禁止缓冲计数，1: 允许缓冲计数
	LONG OutputDir;			// 计数输出电平方向
	LONG bCoutinue;			// 溢出后是否继续计数
	LONG OutputType;		// 定时器脉冲发生方式下有效，输出波形类型。
} USB5935_PARA_CNT, *PUSB5935_PARA_CNT;

//***********************************************************
// 硬件参数USB5935_PARA_CNT中的FunctionMode功能模式选项
const long USB5935_FUNCMODE_COUNTER		= 0x00;	// 计数器模式
const long USB5935_FUNCMODE_TIMER		= 0x01;	// 脉冲定时发生器模式

//***********************************************************
// 硬件参数USB5935_PARA_CNT中的ClockSource功能模式选项
const long USB5935_CLOCKSRC_LOCAL_CLK	= 0x00;	// 板卡局部分频时钟(对40M晶振分频而得,由SetLocalCLKFreq设定)
const long USB5935_CLOCKSRC_CLOCK_IN	= 0x01;	// 外部时钟信号源输入(SOURCE)

//***********************************************************
// 硬件参数USB5935_PARA_CNT中的GateMode在门控模式选项
const long USB5935_GATEMODE_UNUSE_0		= 0x00;		// COUNTER:不使用门控信号(适用于简单事件计数)
													// TIMER:不使用GATE的单次脉冲发生(适用于单次脉冲发生器)
const long USB5935_GATEMODE_RISING_1	= 0x01;		// COUNTER:GATE上边沿触发计数，后续边沿无效
													// TIMER:GATE上边沿单次触发脉冲发生(适用于单次触发单脉冲发生器)
const long USB5935_GATEMODE_FALLING_2	= 0x02;		// COUNTER:GATE下边沿触发,后续边沿无效
													// TIMER:GATE下边沿单次触发脉冲发生(适用于单次触发单脉冲发生器)
const long USB5935_GATEMODE_POSITIVE_3	= 0x03;		// COUNTER:高电平有效(适用于门控事件计数)
													// TIMER:GATE上边沿重复触发脉冲发生(适用于重复触发单脉冲发生器)
const long USB5935_GATEMODE_NEGATIVE_4	= 0x04;		// COUNTER:低电平有效(适用于门控事件计数)
													// TIMER:GATE下边沿重复触发脉冲发生(适用于重复触发单脉冲发生器)
const long USB5935_GATEMODE_RSTART_FSTOP_5	= 0x05;	// COUNTER:上边沿触发计数、下边沿停止计数(适用于单脉冲宽度测量)
													// TIMER:GATE上边沿单次触发连续脉冲串发生器
const long USB5935_GATEMODE_FSTART_RSTOP_6	= 0x06;	// COUNTER:下边沿触发计数、上边沿停止计数(适用于单脉冲宽度测量)
													// TIMER:GATE下边沿单次触发连续脉冲串发生器
const long USB5935_GATEMODE_PSTART_PSTOP_7	= 0x07;	// COUNTER:上边沿触发计数、下一个上边沿停止计数(适用于单周期测量)
													// TIMER:GATE高电平允许连续脉冲串发生器
const long USB5935_GATEMODE_NSTART_NSTOP_8	= 0x08;	// COUNTER:下边沿触发计数、下一个下边沿停止计数(适用于单周期测量)
													// TIMER:GATE低电平允许连续脉冲串发生器

// 硬件参数USB5935_PARA_CNT中的OutputDir在输出方向选项
const long USB5935_OUTPUTDIR_NEGATIVE		= 0x00;	// 禁止计数情况下，输出低电平有效
const long USB5935_OUTPUTDIR_POSITIVE		= 0x01;	// 禁止计数情况下，输出高电平有效

// 硬件参数USB5935_PARA_CNT中的OutputType在输出类型选项
const long USB5935_OUTPUTTYPE_TOGGLE		= 0x00;	// 占空比可设定波形方式(可由InitValue和WidthValue两个参数在定时器脉冲发生方式下设置波形占空比)
const long USB5935_OUTPUTTYPE_PULSE			= 0x01;	// 脉冲方式

//***********************************************************
// CreateFileObject中的Mode参数使用的文件操作方式控制字(可通过或指令实现多种方式并操作)
const long	USB5935_modeRead			= 0x0000;   // 只读文件方式
const long  USB5935_modeWrite			= 0x0001;   // 只写文件方式
const long 	USB5935_modeReadWrite		= 0x0002;   // 既读又写文件方式
const long  USB5935_modeCreate			= 0x1000;   // 如果文件不存可以创建该文件，如果存在，则重建此文件，并清0

//***********************************************************
// 驱动函数接口
#ifndef _USB5935_DRIVER_
#define DEVAPI __declspec(dllimport)
#else
#define DEVAPI __declspec(dllexport)
#endif

#ifdef __cplusplus
extern "C" {
#endif
	//######################## 常规通用函数 #################################
	HANDLE DEVAPI FAR PASCAL USB5935_CreateDevice(int DeviceLgcID = 0); // 创建设备对象(该函数使用系统内逻辑设备ID）
	HANDLE DEVAPI FAR PASCAL USB5935_CreateDeviceEx(int DevicePhysID = 0); // 创建设备对象(该函数使用板卡物理设备ID）
	int DEVAPI FAR PASCAL USB5935_GetDeviceCount(HANDLE hDevice);      // 取得USB5935在系统中的设备数量
	BOOL DEVAPI FAR PASCAL USB5935_GetDeviceCurrentID(HANDLE hDevice, PLONG DeviceLgcID, PLONG DevicePhysID); // 取得当前设备的逻辑ID号和物理ID号
	BOOL DEVAPI FAR PASCAL USB5935_ListDeviceDlg(void); // 用对话框列表系统当中的所有USB5935设备
	BOOL DEVAPI FAR PASCAL USB5935_ResetDevice(HANDLE hDevice);		 // 复位整个USB设备
    BOOL DEVAPI FAR PASCAL USB5935_ReleaseDevice(HANDLE hDevice);    // 释放设备

	//####################### AD数据读取函数 #################################
    BOOL DEVAPI FAR PASCAL USB5935_InitDeviceAD(				// 初始化设备,当返回TRUE后,设备即刻开始传输.
									HANDLE hDevice,				// 设备句柄,它应由CreateDevice函数创建
									PUSB5935_PARA_AD pADPara);  // 硬件参数, 它仅在此函数中决定硬件状态							

    BOOL DEVAPI FAR PASCAL USB5935_ReadDeviceAD(				// 初始化设备后，即可用此函数读取设备上的AD数据
									HANDLE hDevice,				// 设备句柄,它应由CreateDevice函数创建
									USHORT ADBuffer[],			// 将用于接受数据的用户缓冲区
									LONG nReadSizeWords,		// 读取AD数据的长度(字)  
									PLONG nRetSizeWords = NULL);// 实际返回数据的长度(字)

    BOOL DEVAPI FAR PASCAL USB5935_ReleaseDeviceAD(HANDLE hDevice); // 停止AD采集，释放AD对象所占资源

   	//################# AD的硬件参数操作函数 ########################	
	BOOL DEVAPI FAR PASCAL USB5935_SaveParaAD(HANDLE hDevice, PUSB5935_PARA_AD pADPara);  
    BOOL DEVAPI FAR PASCAL USB5935_LoadParaAD(HANDLE hDevice, PUSB5935_PARA_AD pADPara);
    BOOL DEVAPI FAR PASCAL USB5935_ResetParaAD(HANDLE hDevice, PUSB5935_PARA_AD pADPara); // 将AD采样参数恢复至出厂默认值

	//##################### 计数器控制函数 ##########################
    BOOL DEVAPI FAR PASCAL USB5935_InitDeviceCNT(				// 初始化计数器
									HANDLE hDevice,				// 设备句柄
									PUSB5935_PARA_CNT pCNTPara); // 计数器控制字

	ULONG DEVAPI FAR PASCAL USB5935_SetLCLKFreqCNT(			// 设置本地时钟频率(LCLK=Local Clock),返回实际的分频数
									HANDLE hDevice,			// 设备对象句柄,它由CreateDevice函数创建
									double Frequency);		// 时钟频率值

	BOOL DEVAPI FAR PASCAL USB5935_SetDeviceCNT(			// 设置计数器的初值
									HANDLE hDevice,			// 设备对象句柄,它由CreateDevice函数创建
									ULONG CNTVal,			// 计数初值, COUNTER: 计数初值，TIMER:延时初始脉冲宽度(246位)
									ULONG WidthVal);		// 宽度初值, COUNTER: 无效， TIMER:输出脉冲宽度(24位)

	BOOL DEVAPI FAR PASCAL USB5935_GetDeviceCNT(			// 取得各路计数器的当前计数值
									HANDLE hDevice,			// 设备对象句柄,它由CreateDevice函数创建
									PULONG pCNTVal,			// 返回计数值
									PULONG pWidthVal);		// 返回宽度值

	BOOL DEVAPI FAR PASCAL USB5935_GetDevStatusCNT(			// 获得计数器状态
									HANDLE hDevice,			// 设备对象句柄,它由CreateDevice函数创建
									PBOOL bOverflow,		// 获得的计数器溢出标志, =TRUE:表示计数器已溢出, =FALSE:表示未溢出
									PBOOL bBufferRefresh,	// 获得的计数器缓冲更新标志, =TRUE:表示缓冲已被更新, =FALSE:表示未更新
									PBOOL bBufferLost);		// 获得的计数器缓冲丢失标志, =TRUE:表示缓冲已被丢失, =FALSE:表示未丢失

	BOOL DEVAPI FAR PASCAL USB5935_ClrDevStatusCNT(			// 清除计数器状态
									HANDLE hDevice,			// 设备对象句柄,它由CreateDevice函数创建
									BOOL bClrOverflow,		// 是否清除计数器溢出标志, =TRUE:表示清除, =FALSE:表示不清除
									BOOL bClrBufferRefresh,	// 是否清除计数器缓冲更新标志, =TRUE:表示清除, =FALSE:表示不清除
									BOOL bClrBufferLost);	// 是否清除计数器缓冲丢失标志, =TRUE:表示清除, =FALSE:表示不清除

	BOOL DEVAPI FAR PASCAL USB5935_ReleaseDeviceCNT(		// 释放和停止计数/定时器
									HANDLE hDevice);		// 设备对象句柄,它由CreateDevice函数创建

	//####################### 数字I/O输入输出函数 #################################
	BOOL DEVAPI FAR PASCAL USB5935_GetDeviceDI(					// 取得开关量状态     
									HANDLE hDevice,				// 设备句柄,它应由CreateDevice函数创建								        
									BYTE bDISts[6]);			// 开关输入状态(注意: 必须定义为8个字节元素的数组)

    BOOL DEVAPI FAR PASCAL USB5935_SetDeviceDO(					// 输出开关量状态
									HANDLE hDevice,				// 设备句柄,它应由CreateDevice函数创建								        
									BYTE bDOSts[6]);			// 开关输出状态(注意: 必须定义为8个字节元素的数组)

	//############################################################################
	BOOL DEVAPI FAR PASCAL USB5935_GetDevVersion(				// 获取设备固件及程序版本
									HANDLE hDevice,				// 设备对象句柄,它由CreateDevice函数创建
									PULONG pulFmwVersion,		// 固件版本
									PULONG pulDriverVersion);	// 驱动版本

   	//########################## 文件操作函数 ####################################
    HANDLE DEVAPI FAR PASCAL USB5935_CreateFileObject(			// 创建文件对象
									HANDLE hDevice,				// 设备句柄,它应由CreateDevice函数创建
									LPCTSTR strFileName,		// 路径及文件名
									int Mode);					// 文件操作方式

    BOOL DEVAPI FAR PASCAL USB5935_WriteFile(					// 保存用户空间中数据到磁盘文件
									HANDLE hFileObject,			// 文件句柄,它应由CreateFileObject函数创建
									PVOID pDataBuffer,			// 用户数据空间地址
									LONG nWriteSizeBytes);		// 缓冲区大小(字节)

    BOOL DEVAPI FAR PASCAL USB5935_ReadFile(					// 从磁盘文件中读取数据到用户空间
									HANDLE hFileObject,			// 文件句柄,它应由CreateFileObject函数创建
									PVOID pDataBuffer,			// 接受文件数据的用户内存缓冲区
									LONG OffsetBytes,			// 从文件前端开始的偏移位置
									LONG nReadSizeBytes);		// 从偏移位置开始读的字节数

	BOOL DEVAPI FAR PASCAL USB5935_SetFileOffset(				// 设置文件偏移指针
									HANDLE hFileObject,			// 文件句柄,它应由CreateFileObject函数创建
									LONG nOffsetBytes);			// 文件偏移位置（以字为单位）  

	ULONGLONG DEVAPI FAR PASCAL USB5935_GetFileLength(HANDLE hFileObject); // 取得指定文件长度（字节）

    BOOL DEVAPI FAR PASCAL USB5935_ReleaseFile(HANDLE hFileObject);
    LONGLONG DEVAPI FAR PASCAL USB5935_GetDiskFreeBytes(		// 获得指定盘符的磁盘空间(注意使用64位变量)
								   LPCTSTR strDiskName);		// 盘符名,如C盘为"C:\\", D盘为"D:\\"

	//############################ 线程操作函数 ################################
	HANDLE DEVAPI FAR PASCAL USB5935_CreateSystemEvent(void); 	// 创建内核系统事件对象
	BOOL DEVAPI FAR PASCAL USB5935_ReleaseSystemEvent(HANDLE hEvent); // 释放内核事件对象
	BOOL DEVAPI FAR PASCAL USB5935_CreateVBThread(HANDLE* hThread, LPTHREAD_START_ROUTINE RoutineAddr);
	BOOL DEVAPI FAR PASCAL USB5935_TerminateVBThread(HANDLE hThread);

	//################# 其他附加函数 ########################
	BOOL DEVAPI FAR PASCAL USB5935_kbhit(void); // 探测用户是否有击键动作(在控制台应用程序Console中且在非VC语言中)
	char DEVAPI FAR PASCAL USB5935_getch(void); // 等待并获取用户击键值(在控制台应用程序Console中有效)

#ifdef __cplusplus
}
#endif

//#################### 辅助常量 #####################

const long USB5935_MAX_AD_CHANNELS = 16;

#ifndef _USB5935_FIFO_LENGTH_
#define _USB5935_FIFO_LENGTH_
// 本卡可以支持的各种FIFO存储器的长度(点)
const long FIFO_IDT7202_LENGTH				= 1024;
const long FIFO_IDT7203_LENGTH				= 2048;
const long FIFO_IDT7204_LENGTH				= 4096;
const long FIFO_IDT7205_LENGTH				= 8192;
const long FIFO_IDT7206_LENGTH				= 16384;
const long FIFO_IDT7207_LENGTH				= 32768;
#endif; // _USB5935_FIFO_LENGTH_

// 自动包含驱动函数导入库
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