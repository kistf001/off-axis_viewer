#include <algorithm>
#include <iostream>
#include <thread>
#include <vector>
#include <mutex>  // mutex 를 사용하기 위해 필요
#include <cmath>

#include <omp.h>
#include <time.h>
#include <stdio.h> 
#include <string.h>
#include <unistd.h>
#include <sys/types.h> 
#include <netinet/in.h>
#include <sys/socket.h>
#include <arpa/inet.h>

#include <opencv2/core.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/calib3d.hpp>
#include "opencv2/imgcodecs.hpp"
#include "opencv2/imgproc/imgproc.hpp"

//using namespace std;
using namespace cv;

char udp_server_parsing(char *_input_msg, char *_output_msg){
	
    const char instruction[5][4] = { "REQ",	// 동작요청
                                     "PPS",	// 점 초기 위치 지정
                                     "ORG",	// 수정전 점 요청
                                     "AYO",	// 카메라가 맞는지 확인용
                                     "PPP"};	// 자세 요청
	
	char msg_buffer[4] = {'\0',};
    
    // 클라이언트에서 받은 값을 인스트럭션에 매칭한다.
	strncpy(msg_buffer,_input_msg,3);

	if ( strcmp(msg_buffer, instruction[0]) == 0 ) {
		return 'a';
	}
	else if ( strcmp(msg_buffer, instruction[1]) == 0 ) {
		return 'a';
	}
	else if ( strcmp(msg_buffer, instruction[2]) == 0 ) {
		return 'a';
	}
	else if ( strcmp(msg_buffer, instruction[3]) == 0 ) {
		return 'a';
	}
	else if ( strcmp(msg_buffer, instruction[4]) == 0 ) {
		return 'a';
	}

    return 'a';
    
}

void euclidean_distance_Matcher(
    std::vector<Point2f> &prev_v, std::vector<Point2f> new_v, double factory_size){
    
    int* pfloat = new int[new_v.size()];
    
	for(int j = 0; j < new_v.size(); j++) pfloat[j] = 0;
    
	for(int i = 0; i < prev_v.size(); i++){

        double distance_prev = 1.0e+32F;

        int afadsf = 0;

        double a, q;

		for(int j = 0; j < new_v.size(); j++){

			double x = (double)(new_v[j].x - prev_v[i].x);
			double y = (double)(new_v[j].y - prev_v[i].y);

			double distance = (x*x) + (y*y);

			if( ( distance_prev > distance ) && !pfloat[j] ){
                pfloat[afadsf] = 0;
                pfloat[j] = 1;
				distance_prev = distance;
				a = new_v[j].x;
				q = new_v[j].y;
                afadsf = j;
			}

		}
            
		prev_v[i].x = a;
		prev_v[i].y = q;

	}

	delete[] pfloat;

}
void custom_solve_pnp(
    std::vector<Point3f> &objectPoints, std::vector<Point2f> &head_LED_position){
    
}

cv::VideoCapture device_setting_and_init(){
  
	VideoCapture cap1(0);
	
	if (!cap1.isOpened()) printf("첫번째 카메라를 열 수 없습니다.\n");

	cap1.set( 15, 0.1 );
	cap1.set( cv::CAP_PROP_FPS, 75);
    cap1.set( cv::CAP_PROP_BUFFERSIZE, 1);
	cap1.set( cv::CAP_PROP_FRAME_WIDTH , 640 );
	cap1.set( cv::CAP_PROP_FRAME_HEIGHT, 480 );

	cap1.set( cv::CAP_PROP_EXPOSURE, 0.001 );
	cap1.set( cv::CAP_PROP_GAIN, 0.001 );
	cap1.set( cv::CAP_PROP_AUTO_EXPOSURE , 0 );

    for (int i = 0; i < 30; i++) cap1.grab();

    return cap1;
}
std::vector<Point2f> find_center_of_contours(
    std::vector< std::vector<Point> > &contours){

    std::vector<Point2f> raw_pixel_point_buffer;
    
	// 중심 찾기
	if(contours.size() >= 1 ){

        // 등고선 최외각 부분과 최내가ㅏ
		for(int a = 0; a<contours.size(); a++){
			int point_1[2] = {0,};
			int point_2[2] = {0,};
			point_1[0] = contours[a][0].x; 
			point_1[1] = contours[a][0].y; 
			point_2[0] = contours[a][0].x; 
			point_2[1] = contours[a][0].y; 
			for(int b = 1; b < contours[a].size(); b++){
				if( point_1[0]>contours[a][b].x) point_1[0]=contours[a][b].x;
				if( point_1[1]>contours[a][b].y) point_1[1]=contours[a][b].y;
				if( point_2[0]<contours[a][b].x) point_2[0]=contours[a][b].x;
				if( point_2[1]<contours[a][b].y) point_2[1]=contours[a][b].y;
			}
			if(raw_pixel_point_buffer.size()<=64){
				raw_pixel_point_buffer.push_back(
					Point2f( (point_2[0]+point_1[0])>>1, (point_2[1]+point_1[1])>>1 )
				);
			}
		}

        //std::cout << raw_pixel_point_buffer << std::endl;
        
	}

    return raw_pixel_point_buffer;

}
void find_pricesion_center(
    cv::Mat &_bgr, std::vector<Point2f> &head_LED_position){

    #define horizontal_size 640
    #define vertical_size 480

	// 원의 정밀한 위치를 찾아낸다.
	int block_size = 32;
	int block_size_half = block_size>>1;

    uchar *data_output = _bgr.data;

	for(int a = 0; a<4; a++){

	    int XY0_POINT_POSITION[2];
	    int XY1_POINT_POSITION[2];
	    int XY2_POINT_POSITION[2];

	    XY0_POINT_POSITION[0] = (int)head_LED_position[a].x-1;
	    XY0_POINT_POSITION[1] = (int)head_LED_position[a].y-1;
	    XY1_POINT_POSITION[0] = (int)head_LED_position[a].x-block_size_half;
	    XY1_POINT_POSITION[1] = (int)head_LED_position[a].y-block_size_half;
	    XY2_POINT_POSITION[0] = (int)head_LED_position[a].x+block_size_half;
	    XY2_POINT_POSITION[1] = (int)head_LED_position[a].y+block_size_half;
        if(XY1_POINT_POSITION[0]<0) XY1_POINT_POSITION[0] = 0;
        if(XY1_POINT_POSITION[1]<0) XY1_POINT_POSITION[1] = 0;
        if(XY2_POINT_POSITION[0]<0) XY2_POINT_POSITION[0] = 0;
        if(XY2_POINT_POSITION[1]<0) XY2_POINT_POSITION[1] = 0;
        if(XY1_POINT_POSITION[0]>horizontal_size) XY1_POINT_POSITION[0] = horizontal_size;
        if(XY1_POINT_POSITION[1]>vertical_size)   XY1_POINT_POSITION[1] = vertical_size;
        if(XY2_POINT_POSITION[0]>horizontal_size) XY2_POINT_POSITION[0] = horizontal_size;
        if(XY2_POINT_POSITION[1]>vertical_size)   XY2_POINT_POSITION[1] = vertical_size;

        int eeee = 0;
        int wwww[2];

        for(int s = XY1_POINT_POSITION[0]; s < XY2_POINT_POSITION[0]; s++){
            if(eeee<data_output[ 640*XY0_POINT_POSITION[1]+s]) wwww[0] = s;
            eeee = data_output[640*XY0_POINT_POSITION[1]+s];
        }

        head_LED_position[a].x = eeee;

        for(int s = XY1_POINT_POSITION[1]; s < XY2_POINT_POSITION[1]; s++){
            if(eeee<data_output[640*s+XY0_POINT_POSITION[0]]) wwww[0] = s;
            eeee = data_output[640*s+XY0_POINT_POSITION[0]];
        }
        
        head_LED_position[a].y = eeee;

	}

    ////  // head_LED_position 값을 읽어서 배열로 저장한다.
    ////  int XY_point_buffer[2];
    ////  XY_point_buffer[0] = (int)head_LED_position[a].x;
    ////  XY_point_buffer[1] = (int)head_LED_position[a].y;
    //
    ////  if( XY_point_buffer[0] < block_size_half ) 
    ////      XY_point_buffer[0] = block_size_half;
    ////  if( XY_point_buffer[1] < block_size_half ) 
    ////      XY_point_buffer[1] = block_size_half;
    ////  if( XY_point_buffer[0] > (horizontal_size-block_size_half) ) 
    ////      XY_point_buffer[0] = horizontal_size-block_size_half;
    ////  if( XY_point_buffer[1] > (vertical_size-block_size_half) ) 
    ////      XY_point_buffer[1] = vertical_size-block_size_half;
    //
    ////  Rect rect(XY_point_buffer[0]-block_size_half, XY_point_buffer[1]-block_size_half, block_size, block_size);
    //
    ////  uchar *data_output = _bgr.data;
    //
    ////  for(int s = 0; s < block_size; s++){
    ////      counter_x +=         data_output[ s+(block_size_half*block_size) ];
    ////      counter_y +=         data_output[ block_size_half+(block_size*s) ];
    ////      buffer_x  += (double)data_output[ s+(block_size_half*block_size) ] * s;
    ////      buffer_y  += (double)data_output[ block_size_half+(block_size*s) ] * s;
    ////      data_output[ s+(block_size_half*block_size) ] = 255;
    ////      data_output[ block_size_half+(block_size*s) ] = 255;
    ////  }
    //
    //
    ////  Mat ROI_IMAGE;
    ////  _bgr[0](rect).copyTo(ROI_IMAGE);
    //
    ////  long counter_x = 0, counter_y = 0;
    //
    ////  double buffer_x=0, buffer_y=0;
    //
    ////  uchar *data_output = ROI_IMAGE[1].data;
    //
    ////  for(int s = 0; s < block_size; s++){
    ////  	counter_x +=         data_output[ s+(block_size_half*block_size) ];
    ////  	counter_y +=         data_output[ block_size_half+(block_size*s) ];
    ////  	buffer_x  += (double)data_output[ s+(block_size_half*block_size) ] * s;
    ////  	buffer_y  += (double)data_output[ block_size_half+(block_size*s) ] * s;
    ////  	data_output[ s+(block_size_half*block_size) ] = 255;
    ////  	data_output[ block_size_half+(block_size*s) ] = 255;
    ////  }
    //
    ////  double fdfd_x = 0, fdfd_y = 0;
    ////  fdfd_x = buffer_x/(double)counter_x;
    ////  fdfd_y = buffer_y/(double)counter_y;
    //
    ////  head_LED_position[a].x = head_LED_position[a].x-(double)block_size_half+fdfd_x;
    ////  head_LED_position[a].y = head_LED_position[a].y-(double)block_size_half+fdfd_y;
    //
    ////  printf( "%f, %f \n",	head_LED_position_buffer[a].x,  head_LED_position_buffer[a].y );
    ////  printf( "%f, %f \n",	head_LED_position[a].x,			head_LED_position[a].y );

}
void get_marker_positon(
    std::vector<Point3f> &objectPoints, std::vector<Point2f> &head_LED_position, 
    float *angle, float *position){
			
	// 바운딩박스에 들어있는 것만 매칭
	// camera parameters
	double k1 = 0.000001, k2 = -0.000004, p1 = -0.000008, p2 = 0.000009;
	//double m[] = { 600.802,0,332.532,  0,599.137,264.219,  0,0,1 };	// intrinsic parameters
	//double m[] = { 320.802,0,240.532,  0,320.137,240.219,  0,0,1 };	// intrinsic parameters
	double m[] = { 
        2571.42857143/4.05,                   0,  320.000,  
                         0,  2571.42857143/4.05,  240.000,  
                         0,                   0,        1 
    };	// intrinsic parameters
	Mat A(3, 3, CV_64FC1, m);						// camera matrix
	double d[] = {k1, k2, p1, p2};		// k1,k2: radial distortion, p1,p2: tangential distortion
	Mat distCoeffs(4, 1, CV_64FC1, d);

	// estimate camera pose
	Mat rvec, tvec;	// rotation & translation vectors
	cv::solvePnP(objectPoints, head_LED_position, A, distCoeffs, rvec, tvec, cv::SOLVEPNP_ITERATIVE);

    
	angle[0] = rvec.at<double>(0,0) + 0.001;
	angle[1] = rvec.at<double>(1,0) + 0.001;
	angle[2] = rvec.at<double>(2,0) + 0.001;

	position[0] = tvec.at<double>(0,0) + 0.001;
	position[1] = tvec.at<double>(1,0) + 0.001;
	position[2] = tvec.at<double>(2,0) + 0.001;

}

//
std::mutex q, m, a, s;  // 우리의 mutex 객체
cv::VideoCapture cap1;
cv::Mat raw_image;
cv::Mat color_splited_image[3];
cv::Mat thresholded_image[3];
std::vector<Point2f> head_LED_position(4);
bool head_LED_position_changed_flag = 0;

//
float position[3];
float angle[3];
float position_offset[3];
float angle_offset[3];

// 쓰레드를 위한 함수
void thread_function_loop(){

    struct timespec start, end ;

    Mat dfkdfl;

    std::vector<Point3f> objectPoints;
    objectPoints.push_back(Point3f( (-3.75)/2, ( 2.00)/2, 0.0 )); // 40 75
    objectPoints.push_back(Point3f( ( 3.75)/2, ( 2.00)/2, 0.0 ));
    objectPoints.push_back(Point3f( ( 3.75)/2, (-2.00)/2, 0.0 ));
    objectPoints.push_back(Point3f( (-3.70)/2, (-2.00)/2, 0.0 ));

    q.lock(), std::cout << "started main loop"  << std::endl, q.unlock();

	while(1){
		
        m.lock(), dfkdfl = raw_image, m.unlock();

		// 색상분리
        split(dfkdfl, color_splited_image);

        //// 병렬처리  https://swstar.tistory.com/207 
        //#pragma omp parallel 
        //{ // 병렬 구간 시작 
        //    // 각 스레드의 ID 
        //    int tid = omp_get_thread_num(); 
        //    if (tid == 0) 
        //    { 
        //        /* 스레드 ID가 0인 경우에 한해, 
        //        * 스레드의 총 갯수 출력 */ 
        //        int n_thread = omp_get_num_threads(); 
        //        fprintf(stdout, " n_thread = %d\n", n_thread); 
        //    } 
        //
        //    // 스레드 동기화 
        //    #pragma omp barrier 
        //
        //    /* 스레드들이 서로 간섭하지 않도록 
        //     * 코드 블록을 격리 */ 
        //    #pragma omp critical 
        //    { // 격리 구간 시작 
        //        fprintf(stdout, "[THREAD %d] : Hello World!\n", tid); 
        //        sum += 1; 
        //        fprintf(stdout, "[THREAD %d] : sum now = %d\n", tid, sum); 
        //    } // 격리 구간 끝 
        //
        //} // 병렬 구간 끝

		// 색상 분리된 이미지를 이진화
		threshold(color_splited_image[0], thresholded_image[0], 210, 255, THRESH_BINARY ); 
		//threshold(color_splited_image[1], thresholded_image[1], 210, 255, THRESH_BINARY ); 
		//threshold(color_splited_image[2], thresholded_image[2], 210, 255, THRESH_BINARY );

		// 외곽선 찾기
        std::vector< std::vector<Point> > contours[3];
    	findContours( thresholded_image[0], contours[0], RETR_TREE, CHAIN_APPROX_SIMPLE );
    	//findContours( thresholded_image[1], contours[1], RETR_TREE, CHAIN_APPROX_SIMPLE );
    	//findContours( thresholded_image[2], contours[2], RETR_TREE, CHAIN_APPROX_SIMPLE );

        // 등고선의 중앙의 점으로 나타내게 연산해서 바꿈
        std::vector<Point2f> center_point0 = find_center_of_contours(contours[0]);
        //std::vector<Point2f> center_point1 = find_center_of_contours(contours[1]);
        //std::vector<Point2f> center_point2 = find_center_of_contours(contours[2]);

        // 센터포인트가 존재하는지 확인하고
        if(center_point0.size()>=4){
            
            static std::vector<Point2f> head_LED_position__(4);
            static float position__[3], angle__[3];

            // 정확한 점 위치를 찾음
            //find_pricesion_center(color_splited_image[0], center_point0);
            
            // 유클라디안 거리 매칭을 통해서 순서를 맞춰줌
            euclidean_distance_Matcher( head_LED_position__, center_point0, 20 );
            get_marker_positon(objectPoints, head_LED_position__, position__, angle__);

            static float x_est_last[6];
            static float P_last[6];

            static float Q[6] = {0.022,0.022,0.022,0.0022,0.0022,0.0022};
            static float R[6] = {0.617,0.617,0.617,0.0617,0.0617,0.0617};
            static float K[6];
            static float P[6];
            static float P_temp[6];
            static float x_temp_est[6];
            static float x_est[6];

            static float z_measured[6];
            //#the 'noisy' value we measured
            static float z_real[6];
            //#the ideal value we wish to measure
            //#initialize with a measurement

            /*****************************KALMAN FILTER*******************************/ 
            z_real[0] = position__[0];
            z_real[1] = position__[1];
            z_real[2] = position__[2];
            z_real[3] = angle__[0];
            z_real[4] = angle__[1];
            z_real[5] = angle__[2];

            for(int U=0; U<6; U++){
                //#   do a prediction    #
                x_temp_est[U] = x_est_last[U];
                P_temp[U] = P_last[U] + Q[U];
                //#   calculate the Kalman gain
                K[U] = P_temp[U] * (1.0/(P_temp[U] + R[U]));
                //#   measure
                z_measured[U] = z_real[U];
                //#   the real measurement plus noise
                //#   correct
                x_est[U] = x_temp_est[U] + K[U] * (z_measured[U] - x_temp_est[U]);
                P[U] = (1-K[U]) * P_temp[U];
                //#   update our last's         
                P_last[U] = P[U];
                x_est_last[U] = x_est[U];
            }

            position__[0] = x_est[0];
            position__[1] = x_est[1];
            position__[2] = x_est[2];
            angle__[0] = x_est[3];
            angle__[1] = x_est[4];
            angle__[2] = x_est[5];
            
            /*************************************************************************/ 
            
            if(s.try_lock()) {
                if(head_LED_position_changed_flag){
                    head_LED_position__ = head_LED_position;
                    head_LED_position_changed_flag = 0;
                }
                s.unlock();
            }
            if(a.try_lock()) {
                position[0]=position__[0];
                position[1]=position__[1];
                position[2]=position__[2];
                angle[0]=angle__[0];
                angle[1]=angle__[1];
                angle[2]=angle__[2];
                a.unlock();
            }
            
        }

        clock_gettime(CLOCK_MONOTONIC, &end);
        //eeeeeeee = 1/((end.tv_nsec - start.tv_nsec) / 1000000000.0);
        clock_gettime(CLOCK_MONOTONIC, &start);
    
    }

}
void thread_function_get_image_from_driver(){

    struct timespec start, end ;
    
    q.lock(), std::cout << "started capture loop"  << std::endl, q.unlock();

    while (1) {
        
        cap1.grab();

        if(m.try_lock()) cap1.retrieve(raw_image), m.unlock();
        
        clock_gettime(CLOCK_MONOTONIC, &end);
        //qqqqqqqq = 1/((end.tv_nsec - start.tv_nsec) / 1000000000.0);
        clock_gettime(CLOCK_MONOTONIC, &start);

    }

}
void thread_function_udp_server(){

    struct timespec start, end ;

    #define UDP_PORT 5100

	int sockfd,Recv_Size;
	struct sockaddr_in servaddr, cliaddr;
	socklen_t len;
	char mesg[512], mesgs[28];
	sockfd=socket(AF_INET, SOCK_DGRAM, 0); //UDP를 위한 소켓 생성

	//접속 되는 클라이언트를 위한 주소 설정 후 운영체제에 서비스 등록
	memset(&servaddr, 0, sizeof(servaddr));
	servaddr.sin_family=AF_INET;
	servaddr.sin_addr.s_addr=htonl(INADDR_ANY);
	servaddr.sin_port=htons(UDP_PORT);
	bind(sockfd, (struct sockaddr *)&servaddr, sizeof(servaddr));

    q.lock(), std::cout << "started UDP loop"  << std::endl, q.unlock();

	while(1){

        a.lock(); 
        float position_buf[3] = { 
            position[0]-position_offset[0], 
            position[1]-position_offset[1], 
            position[2]-position_offset[2] 
        };
        float angle_buf[3] = {
            angle[0]-angle_offset[0],
            angle[1]-angle_offset[1],
            angle[2]-angle_offset[2]
        };
        a.unlock();

        //    Xp,Yp,Zp[0:12]    Xr,Yr,Zr[0:12]    TIME[0:4]

        mesgs[ 0]=*(long*)&position_buf[0]>>24; 
        mesgs[ 1]=*(long*)&position_buf[0]>>16; 
        mesgs[ 2]=*(long*)&position_buf[0]>> 8; 
        mesgs[ 3]=*(long*)&position_buf[0]    ; 
        mesgs[ 4]=*(long*)&position_buf[1]>>24; 
        mesgs[ 5]=*(long*)&position_buf[1]>>16; 
        mesgs[ 6]=*(long*)&position_buf[1]>> 8; 
        mesgs[ 7]=*(long*)&position_buf[1]    ; 
        mesgs[ 8]=*(long*)&position_buf[2]>>24; 
        mesgs[ 9]=*(long*)&position_buf[2]>>16; 
        mesgs[10]=*(long*)&position_buf[2]>> 8; 
        mesgs[11]=*(long*)&position_buf[2]    ; 

        mesgs[12]=*(long*)&angle_buf[0]>>24; 
        mesgs[13]=*(long*)&angle_buf[0]>>16; 
        mesgs[14]=*(long*)&angle_buf[0]>> 8; 
        mesgs[15]=*(long*)&angle_buf[0]    ; 
        mesgs[16]=*(long*)&angle_buf[1]>>24; 
        mesgs[17]=*(long*)&angle_buf[1]>>16; 
        mesgs[18]=*(long*)&angle_buf[1]>> 8; 
        mesgs[19]=*(long*)&angle_buf[1]    ; 
        mesgs[20]=*(long*)&angle_buf[2]>>24; 
        mesgs[21]=*(long*)&angle_buf[2]>>16; 
        mesgs[22]=*(long*)&angle_buf[2]>> 8; 
        mesgs[23]=*(long*)&angle_buf[2]    ; 

        mesgs[24]='b';
        mesgs[25]='b';
        mesgs[26]='b';
        mesgs[27]='b';

		Recv_Size = recvfrom(sockfd, mesg, 512, 0, (struct sockaddr *)&cliaddr, &len);

		sendto( sockfd, mesgs, 28, 0,(struct sockaddr *)&cliaddr, sizeof(cliaddr));

        //std::cout << "UDP requested"  << std::endl;
        
		usleep(1000);

        clock_gettime(CLOCK_MONOTONIC, &end);
        //eeeeeeee = (end.tv_nsec - start.tv_nsec) / 1000000000.0;
        clock_gettime(CLOCK_MONOTONIC, &start);

	}

	close(sockfd);

}
void thread_function_tcp_server(){

    struct timespec start, end ;
    
    int serv_sock, clnt_sock;
   
    //sockaddr_in은 소켓 주소의 틀을 형셩해주는 구조체로 AF_INET일 경우 사용
    struct sockaddr_in serv_addr;
    struct sockaddr_in clnt_addr; //accept함수에서 사용됨.
    socklen_t clnt_addr_size;
    
    //주소를 초기화한 후 IP주소와 포트 지정
    memset(&serv_addr, 0, sizeof(serv_addr)); 
    serv_addr.sin_family=AF_INET;                //타입: ipv4
    serv_addr.sin_addr.s_addr=htonl(INADDR_ANY); //ip주소
    serv_addr.sin_port=htons(10200);     //port
   
    //TCP연결지향형이고 ipv4 도메인을 위한 소켓을 생성
    serv_sock = socket(PF_INET, SOCK_STREAM, 0); 
    
    //소켓과 서버 주소를 바인딩
    bind(serv_sock, (struct sockaddr*) &serv_addr, sizeof(serv_addr));
    
    //연결 대기열 5개 생성 
    listen(serv_sock, 5);
    
    q.lock(), std::cout << "started TCP loop"  << std::endl, q.unlock();

    int recived_data_length;
    char buf[512];
    std::vector<uchar> buffer;
    cv::Mat image_copy;
    
    while (1) {

        //클라이언트로부터 요청이 오면 연결 수락
        clnt_addr_size = sizeof(clnt_addr);
        clnt_sock      = accept(serv_sock, (struct sockaddr*)&clnt_addr, &clnt_addr_size);

        /*-----클라이언트로 받은 첫번째 데이터-----*/

        recived_data_length = read(clnt_sock, buf, 512);
        
        // 메인 이미지 버퍼에서 이미지를 복사해온 다음에 jpg byte stream으로 변환
        if(  (buf[0]=='R')  ==  (buf[1]=='A')  ==  (buf[2]=='W')  ) 
            image_copy = raw_image;
        else if(  (buf[0]=='S')  ==  (buf[1]=='P')  ==  (buf[2]=='L')  )
            image_copy = color_splited_image[0];
        else if(  (buf[0]=='B')  ==  (buf[1]=='I')  ==  (buf[2]=='N')  )
            image_copy = thresholded_image[0];
        
        cv::imencode(".png", image_copy, buffer);

        /*-----데이터 전송-----*/
        write(clnt_sock, reinterpret_cast<char*>(buffer.data()), buffer.size());
        
        // 전송 완료후 클라이언트 소켓 닫기
        close(clnt_sock);

        buffer.clear();

        usleep(100000);
        
        clock_gettime(CLOCK_MONOTONIC, &end);
        //eeeeeeee = (end.tv_nsec - start.tv_nsec) / 1000000000.0;
        clock_gettime(CLOCK_MONOTONIC, &start);

    }
    
    close(serv_sock);

}
void thread_function_tcp_setup(){

    struct timespec start, end ;
    
    int serv_sock, clnt_sock;
   
    //sockaddr_in은 소켓 주소의 틀을 형셩해주는 구조체로 AF_INET일 경우 사용
    struct sockaddr_in serv_addr;
    struct sockaddr_in clnt_addr;                //accept함수에서 사용됨.
    socklen_t clnt_addr_size;
    
    //주소를 초기화한 후 IP주소와 포트 지정
    memset(&serv_addr, 0, sizeof(serv_addr)); 
    serv_addr.sin_family=AF_INET;                //타입: ipv4
    serv_addr.sin_addr.s_addr=htonl(INADDR_ANY); //ip주소
    serv_addr.sin_port=htons(20400);             //port
   
    //TCP연결지향형이고 ipv4 도메인을 위한 소켓을 생성
    serv_sock = socket(PF_INET, SOCK_STREAM, 0); 
    
    //소켓과 서버 주소를 바인딩
    bind(serv_sock, (struct sockaddr*) &serv_addr, sizeof(serv_addr));
    
    //연결 대기열 5개 생성 
    listen(serv_sock, 5);
    
    q.lock(), std::cout << "setup TCP loop"  << std::endl, q.unlock();
        
    while (1) {

        /*-----클라이언트로부터 요청이 오면 연결 수락-----*/
        clnt_addr_size = sizeof(clnt_addr);
        clnt_sock      = accept(serv_sock, (struct sockaddr*)&clnt_addr, &clnt_addr_size);

        /*-----클라이언트로 받은 첫번째 데이터-----*/
        static char buf[512]; 
        read(clnt_sock, buf, 512);

        if((buf[ 0]=='R')){
            static std::vector<Point2f> WWWWWWWWWWWWWW(4);
            WWWWWWWWWWWWWW[0].x = (buf[ 0+4]<<24) | (buf[ 1+4]<<16) | (buf[ 2+4]<<8) | buf[ 3+4];
            WWWWWWWWWWWWWW[0].y = (buf[ 4+4]<<24) | (buf[ 5+4]<<16) | (buf[ 6+4]<<8) | buf[ 7+4];
            WWWWWWWWWWWWWW[1].x = (buf[ 8+4]<<24) | (buf[ 9+4]<<16) | (buf[10+4]<<8) | buf[11+4];
            WWWWWWWWWWWWWW[1].y = (buf[12+4]<<24) | (buf[13+4]<<16) | (buf[14+4]<<8) | buf[15+4];
            WWWWWWWWWWWWWW[2].x = (buf[16+4]<<24) | (buf[17+4]<<16) | (buf[18+4]<<8) | buf[19+4];
            WWWWWWWWWWWWWW[2].y = (buf[20+4]<<24) | (buf[21+4]<<16) | (buf[22+4]<<8) | buf[23+4];
            WWWWWWWWWWWWWW[3].x = (buf[24+4]<<24) | (buf[25+4]<<16) | (buf[26+4]<<8) | buf[27+4];
            WWWWWWWWWWWWWW[3].y = (buf[28+4]<<24) | (buf[29+4]<<16) | (buf[30+4]<<8) | buf[31+4];
            s.lock();
            head_LED_position = WWWWWWWWWWWWWW;
            head_LED_position_changed_flag = 1;
            s.unlock();
        }
        if((buf[ 0]=='S')){
            a.lock(); 
            for (int a = 0; a<3; a++) position_offset[a]=position[a], angle_offset[a]=angle[a];
            a.unlock();
        }

        /*-----데이터 전송-----*/
        char snedData[123];
        write(clnt_sock, snedData, 28);
        
        /*-----데이터 전송 완료후 클라이언트 소켓 닫기-----*/
        close(clnt_sock);
        
        clock_gettime(CLOCK_MONOTONIC, &end);
        //eeeeeeee = (end.tv_nsec - start.tv_nsec) / 1000000000.0;
        clock_gettime(CLOCK_MONOTONIC, &start);

    }
    
    close(serv_sock);

}
void thread_function_log_viewer(){

    struct timespec start, end ;

    q.lock(), std::cout << "viewer TCP loop"  << std::endl, q.unlock();

    while(1){
    
        std::cout 
            << "  " << position[0]
            << "  " << position[1]
            << "  " << position[2]
            << "  " << angle[0]
            << "  " << angle[1]
            << "  " << angle[2]
            << "  " << std::endl;

        usleep(500000);
        
        clock_gettime(CLOCK_MONOTONIC, &end);
        //eeeeeeee = (end.tv_nsec - start.tv_nsec) / 1000000000.0;
        clock_gettime(CLOCK_MONOTONIC, &start);

    }
    
}

int main(int, char**){

    cap1=device_setting_and_init();
    cap1.read(raw_image);

    for (int a = 0; a<3; a++) position_offset[a]=0, angle_offset[a]=0;

    // 쓰레드를 선언, node를 파라미터로 넘긴다.
    std::thread _t1(thread_function_loop);
    std::thread _t2(thread_function_get_image_from_driver);
    std::thread _t3(thread_function_udp_server);
    std::thread _t4(thread_function_tcp_server);
    std::thread _t5(thread_function_tcp_setup);
    std::thread _t6(thread_function_log_viewer);

    // 쓰레드가 종료할 때까지 대기
    _t1.join();
    _t2.join();
    _t3.join();
    _t4.join();
    _t5.join();
    _t6.join();

    return 0;

}

/* CAMERA SETTING 
 *
 * User Controls
 *                      brightness 0x00980900 (int)    : min=0 max=100 step=1 default=50 value=50 flags=slider
 *                        contrast 0x00980901 (int)    : min=-100 max=100 step=1 default=0 value=0 flags=slider
 *                      saturation 0x00980902 (int)    : min=-100 max=100 step=1 default=0 value=0 flags=slider
 *                     red_balance 0x0098090e (int)    : min=1 max=7999 step=1 default=1000 value=1000 flags=slider
 *                    blue_balance 0x0098090f (int)    : min=1 max=7999 step=1 default=1000 value=1000 flags=slider
 *                 horizontal_flip 0x00980914 (bool)   : default=0 value=0
 *                   vertical_flip 0x00980915 (bool)   : default=0 value=0
 *            power_line_frequency 0x00980918 (menu)   : min=0 max=3 default=1 value=1
 *                       sharpness 0x0098091b (int)    : min=-100 max=100 step=1 default=0 value=0 flags=slider
 *                   color_effects 0x0098091f (menu)   : min=0 max=15 default=0 value=0
 *                          rotate 0x00980922 (int)    : min=0 max=360 step=90 default=0 value=0 flags=modify-layout
 *              color_effects_cbcr 0x0098092a (int)    : min=0 max=65535 step=1 default=32896 value=32896
 * 
 * Codec Controls
 *              video_bitrate_mode 0x009909ce (menu)   : min=0 max=1 default=0 value=0 flags=update
 *                   video_bitrate 0x009909cf (int)    : min=25000 max=25000000 step=25000 default=10000000 value=10000000
 *          repeat_sequence_header 0x009909e2 (bool)   : default=0 value=0
 *             h264_i_frame_period 0x00990a66 (int)    : min=0 max=2147483647 step=1 default=60 value=60
 *                      h264_level 0x00990a67 (menu)   : min=0 max=11 default=11 value=11
 *                    h264_profile 0x00990a6b (menu)   : min=0 max=4 default=4 value=4
 * 
 * Camera Controls
 *                   auto_exposure 0x009a0901 (menu)   : min=0 max=3 default=0 value=0
 *          exposure_time_absolute 0x009a0902 (int)    : min=1 max=10000 step=1 default=1000 value=1000
 *      exposure_dynamic_framerate 0x009a0903 (bool)   : default=0 value=0
 *              auto_exposure_bias 0x009a0913 (intmenu): min=0 max=24 default=12 value=12
 *       white_balance_auto_preset 0x009a0914 (menu)   : min=0 max=10 default=1 value=1
 *             image_stabilization 0x009a0916 (bool)   : default=0 value=0
 *                 iso_sensitivity 0x009a0917 (intmenu): min=0 max=4 default=0 value=0
 *            iso_sensitivity_auto 0x009a0918 (menu)   : min=0 max=1 default=1 value=1
 *          exposure_metering_mode 0x009a0919 (menu)   : min=0 max=2 default=0 value=0
 *                      scene_mode 0x009a091a (menu)   : min=0 max=13 default=0 value=0
 * 
 * JPEG Compression Controls
 *             compression_quality 0x009d0903 (int)    : min=1 max=100 step=1 default=30 value=30
 * 
 * v4l2-ctl --set-ctrl=brightness=0
 * v4l2-ctl --set-ctrl=auto_exposure=0
 */