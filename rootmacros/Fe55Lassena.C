#include "TFile.h"
#include "TH2.h"
#include "TH1.h"
#include "TMath.h"
#include "iostream"
#include <stdio.h>
#include "Riostream.h"
#include <math.h>
#include <stdlib.h>
#include <string>
#include <algorithm>
#include <TImage.h>
#include "TCanvas.h"

using namespace std;

void GetFrame(FILE *in);
void SomeEvents(TH2F **hitinfos);
void LookDistr(TH1F **signaldistribution);
void GetZoomEvent();
void GetPedestal(TH1F **LuckyDist, TH2F **TwoDHis);
void CheckPixels(TH1F **CheckDist);

int NumberOfWordsDataFile=3360000;

const int NPixX=2400,NPixY=2800;
const int NZoomX=100,NZoomY=100;
float event[NPixX][NPixY];
int Xmin=1750,Ymin=700;
float ZoomEvent[NZoomX][NZoomY];
float pedestal[NZoomX][NZoomY];
double noise[NZoomX][NZoomY];
int NPedEvt=300;

const int NLucky=20;
int LuckyPixel[NLucky][2];
const int NCheck=5;
int CheckPixel[NCheck][2];

int main(){
    
    
    LuckyPixel[0][0]=20;LuckyPixel[0][1]=20;
    LuckyPixel[1][0]=80;LuckyPixel[1][1]=80;
    LuckyPixel[2][0]=80;LuckyPixel[2][1]=20;
    LuckyPixel[3][0]=20;LuckyPixel[3][1]=80;
    LuckyPixel[4][0]=50;LuckyPixel[4][1]=50;
    
    LuckyPixel[5][0]=30;LuckyPixel[5][1]=30;
    LuckyPixel[6][0]=70;LuckyPixel[6][1]=70;
    LuckyPixel[7][0]=80;LuckyPixel[7][1]=30;
    LuckyPixel[8][0]=30;LuckyPixel[8][1]=70;
    LuckyPixel[9][0]=60;LuckyPixel[9][1]=60;
    
    LuckyPixel[10][0]=40;LuckyPixel[10][1]=40;
    LuckyPixel[11][0]=60;LuckyPixel[11][1]=60;
    LuckyPixel[12][0]=60;LuckyPixel[12][1]=40;
    LuckyPixel[13][0]=40;LuckyPixel[13][1]=60;
    LuckyPixel[14][0]=45;LuckyPixel[14][1]=45;
    
    LuckyPixel[15][0]=10;LuckyPixel[15][1]=10;
    LuckyPixel[16][0]=90;LuckyPixel[16][1]=90;
    LuckyPixel[17][0]=90;LuckyPixel[17][1]=10;
    LuckyPixel[18][0]=10;LuckyPixel[18][1]=90;
    LuckyPixel[19][0]=65;LuckyPixel[19][1]=65;
    
    CheckPixel[0][0]=1770;CheckPixel[0][1]=2300;
    CheckPixel[1][0]=1850;CheckPixel[1][1]=2400;
    CheckPixel[2][0]=1850;CheckPixel[2][1]=2300;
    CheckPixel[3][0]=1770;CheckPixel[3][1]=2400;
    CheckPixel[4][0]=1810;CheckPixel[4][1]=2350;

    char fileRoot[180];
    sprintf(fileRoot,"%s","../rootfiles/jaap2.root");
    
    // Make histos
    TFile *fRootHis = new TFile(fileRoot,"RECREATE");
    
    TH2F *hitinfos[5];
    char text[60];
    for (int i=0;i<5;i++) {
        sprintf(text,"%s%d","Hitmap entire sensor event ",i);
        hitinfos[i]=new TH2F(text,text,2400,-.5,2400-0.5,2800,-.5,2800-0.5);
    }
 
    TH1F *LuckyDist[NLucky];
    for (int i=0;i<NLucky;i++) {
        sprintf(text,"%s%d","Lucky pixel ",i);
        LuckyDist[i]=new TH1F(text,text,400,0.,8000);
    }
    TH1F *CheckDist[2*NCheck];
    for (int i=0;i<5;i++) {
        sprintf(text,"%s%d","Check pixel ",i);
        CheckDist[i]=new TH1F(text,text,400,0.,8000);
    }
    for (int i=0;i<5;i++) {
        sprintf(text,"%s%d","Double check pixel ",i);
        CheckDist[i+5]=new TH1F(text,text,400,0.,8000);
    }
    
    TH1F *signaldistribution[4];
    signaldistribution[0]=new TH1F("dist4","dist4",800,0.,16000.);
    signaldistribution[1]=new TH1F("dist10","dist10",800,0.,16000.);
    signaldistribution[2]=new TH1F("dist14","dist14",800,0.,16000.);
    signaldistribution[3]=new TH1F("dist2","dist2",800,0.,16000.);

    TH2F *TwoDHis[2];
    TwoDHis[0]=new TH2F("pedestal","pedestal",NZoomX,-.5,NZoomX-0.5,NZoomY,-.5,NZoomY-0.5);
    TwoDHis[1]=new TH2F("noise","noise",NZoomX,-.5,NZoomX-0.5,NZoomY,-.5,NZoomY-0.5);
    
//    SomeEvents(hitinfos);
//    LookDistr(signaldistribution);
    CheckPixels(CheckDist);
    GetPedestal(LuckyDist,TwoDHis);
    
    
    fRootHis->Write();
    cout<<"wrote "<<fileRoot<<endl;
    cout<<"Klaar"<<endl;
    return 0;
} // end main

//**************************************************
//**************************************************
void GetZoomEvent() {
//**************************************************

    for (int i=0;i<NZoomX;i++) {
        for (int j=0;j<NZoomY;j++) {
            ZoomEvent[i][j]=event[i+Xmin][j+Ymin];
        } // j
    } // i
}
//**************************************************
//**************************************************
void GetPedestal(TH1F **LuckyDist, TH2F **TwoDHis){
//**************************************************
    char datafilename[100];
    
    for (int i=0;i<NZoomX;i++) {
        for (int j=0;j<NZoomY;j++) {
            pedestal[i][j]=0.;
            noise[i][j]=0.;
        } // i
    } // j
    
    for (int iEvt=0;iEvt<NPedEvt;iEvt++){
        sprintf(datafilename,"%s%d%s","../Degrees5p4_dose4/File_5p4degrees4",iEvt,".tiff");
        FILE *in=fopen(datafilename,"rb");
        GetFrame(in); //Xmin=1750,Ymin=700;
//        cout<<"check "<<event[1800][750]<<endl;
        GetZoomEvent();
        fclose(in);
        // lucky pixels
        for (int i=0;i<NLucky;i++) {
            LuckyDist[i]->Fill(ZoomEvent[LuckyPixel[i][0]][LuckyPixel[i][1]],1.);
        } // i
//        cout<<"iEvt="<<iEvt<<"    "<<ZoomEvent[50][50]<<"   "<<ZoomEvent[LuckyPixel[4][0]][LuckyPixel[4][1]]<<endl;
        for (int i=0;i<NZoomX;i++) {
            for (int j=0;j<NZoomY;j++) {
                pedestal[i][j]+=ZoomEvent[i][j];
                noise[i][j]+=(ZoomEvent[i][j]*ZoomEvent[i][j]);
            } // j
        } // i
        
    } // iEvt
    
    for (int i=0;i<NZoomX;i++) {
        for (int j=0;j<NZoomY;j++) {
            pedestal[i][j]=pedestal[i][j]/NPedEvt;
            noise[i][j]=TMath::Sqrt(noise[i][j]/NPedEvt-pedestal[i][j]*pedestal[i][j]);
            TwoDHis[0]->Fill(i,j,pedestal[i][j]);
            TwoDHis[1]->Fill(i,j,noise[i][j]);
        } // j
    } // i
    
}
//**************************************************
//**************************************************
void CheckPixels(TH1F **CheckDist){
//**************************************************
    char datafilename[100];
    
    cout<<"Check"<<endl;
    for (int iEvt=0;iEvt<NPedEvt;iEvt++){
        sprintf(datafilename,"%s%d%s","../Degrees5p4_dose4/File_5p4degrees4",iEvt,".tiff");
        FILE *in=fopen(datafilename,"rb");
        GetFrame(in);
        fclose(in);
        // lucky pixels
        for (int i=0;i<5;i++) {
            CheckDist[i]->Fill(event[CheckPixel[i][0]][CheckPixel[i][1]],1.);
        } // i
    } // iEvt
    
    cout<<"Double check"<<endl;
    for (int iEvt=0;iEvt<NPedEvt;iEvt++){
        sprintf(datafilename,"%s%d%s","../Degrees5p4_dose10/File_5p4degrees10_",iEvt,".tiff");
        FILE *in=fopen(datafilename,"rb");
        GetFrame(in);
        fclose(in);
        // lucky pixels
        for (int i=0;i<5;i++) {
            CheckDist[i+5]->Fill(event[LuckyPixel[i][0]+Xmin][LuckyPixel[i][1]+Ymin],1.);
        } // i
    } // iEvt
    
}
//**************************************************
//**************************************************
void GetFrame(FILE *in){
//**************************************************
    unsigned int Word1=0x00000000;
    unsigned int Word2=0x00000000;
    unsigned int Word3=0x00000000;
    int width=2400/2;
    
    //Get rid of header. Think are 2 words
    fread(&Word1,sizeof(unsigned int),1, in);
    fread(&Word1,sizeof(unsigned int),1, in);
    
    
    int xindex,yindex;
    for (int i=0;i<NumberOfWordsDataFile;i++) {
        fread(&Word1,sizeof(unsigned int),1, in);
        Word2=((Word1&0x0000FF00)>>8);
        Word2+=((Word1&0x000000FF)<<8);
        Word3=((Word1&0xFF000000)>>24);
        Word3+=((Word1&0x00FF0000)>>8);
        //        if (i<50){            cout<<i<<"   "<<hex<<Word3<<"   "<<Word2<<dec<<
        //            "   "<<Word3<<"   "<<Word2<<endl;}
        yindex=int(i/width);
        xindex=2*int(i%width);
        
     
        
        event[xindex][yindex]=Word3*1.;
        event[xindex+1][yindex]=Word2*1.;
        
    } //i
    
    
}
//**************************************************
//**************************************************
void SomeEvents(TH2F **hitinfos){
//**************************************************
    cout<<"Writing out some events"<<endl;
    char datafilename[100];
    for (int FrameNr=0;FrameNr<5;FrameNr++) {
        sprintf(datafilename,"%s%d%s","../Degrees5p4_dose4/File_5p4degrees4",FrameNr,".tiff");
        FILE *in=fopen(datafilename,"rb");
        GetFrame(in);
        fclose(in);
            for (int i=0;i<NPixX;i++) {
            for (int j=0;j<NPixY;j++) {
                hitinfos[FrameNr]->Fill(i,j,event[i][j]);
            } // j
        } // i
    
    } // FrameNr
}
//**************************************************
//**************************************************
void LookDistr(TH1F **signaldistribution){
//**************************************************

    // look at distribution
    char datafilename[100];
    for (int FrameNr=0;FrameNr<100;FrameNr++) {
        if ((FrameNr%30)==0) {cout<<"frame "<<FrameNr<<"    "<<datafilename<<endl;}
        sprintf(datafilename,"%s%d%s","../Degrees5p4_dose4/File_5p4degrees4",FrameNr,".tiff");
        FILE *in=fopen(datafilename,"rb");
        GetFrame(in);
        fclose(in);
        
        for (int i=1750;i<1850;i++) {
            for (int j=700;j<800;j++) {
                signaldistribution[0]->Fill(event[i][j],1.);
            } // j
        } // i
    } // FrameNr

    for (int FrameNr=0;FrameNr<100;FrameNr++) {
        if ((FrameNr%20)==0) {cout<<"frame "<<FrameNr<<"    "<<datafilename<<endl;}
        sprintf(datafilename,"%s%d%s","../Degrees5p4_dose10/File_5p4degrees10_",FrameNr,".tiff");
        FILE *in=fopen(datafilename,"rb");
        GetFrame(in);
        fclose(in);
        for (int i=1750;i<1850;i++) {
            for (int j=700;j<800;j++) {
                signaldistribution[1]->Fill(event[i][j],1.);
            } // j
        } // i
    } // FrameNr


    for (int FrameNr=0;FrameNr<100;FrameNr++) {
        if ((FrameNr%20)==0) {cout<<"frame "<<FrameNr<<"    "<<datafilename<<endl;}
        sprintf(datafilename,"%s%d%s","../Degrees5p4_dose0/File_5p4degrees0",FrameNr,".tiff");
        FILE *in=fopen(datafilename,"rb");
        GetFrame(in);
        fclose(in);
        for (int i=1750;i<1850;i++) {
            for (int j=700;j<800;j++) {
                signaldistribution[2]->Fill(event[i][j],1.);
            } // j
        } // i
    } // FrameNr

    for (int FrameNr=0;FrameNr<100;FrameNr++) {
        if ((FrameNr%20)==0) {cout<<"frame "<<FrameNr<<"    "<<datafilename<<endl;}
        sprintf(datafilename,"%s%d%s","../Degrees38p5_dose2/File_38p5degrees2_",FrameNr,".tiff");
        FILE *in=fopen(datafilename,"rb");
        GetFrame(in);
        fclose(in);
        for (int i=1750;i<1850;i++) {
            for (int j=700;j<800;j++) {
                signaldistribution[3]->Fill(event[i][j],1.);
            } // j
        } // i
    } // FrameNr
    // End distribution
    
}
//**************************************************
//**************************************************
