using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Text.RegularExpressions;
using System.Web;
using System.Web.Mvc;

//It includes 3 parts: UV data, suburb UV data and UV trend
namespace TA42_5120.Controllers
{
    public class DataController : Controller
    {
        public ActionResult Trend()
        {
            ViewBag.Title = "UV Trend in Mel";
            return View();
        }

        public ActionResult SuburbUV()
        {
            ViewBag.Title = "UV Level near CBD";

            //This version of code is using URL
            string urlAddress = "https://lemonumbrella.azurewebsites.net/uvr_inner_suburbs_i3";
            HttpWebRequest request = (HttpWebRequest)WebRequest.Create(urlAddress);
            HttpWebResponse response = (HttpWebResponse)request.GetResponse();
            if (response.StatusCode == HttpStatusCode.OK)
            {
                Stream receiveStream = response.GetResponseStream();
                StreamReader readStream = null;
                if (response.CharacterSet == null)
                    readStream = new StreamReader(receiveStream);
                else
                    readStream = new StreamReader(receiveStream, Encoding.GetEncoding(response.CharacterSet));
                string data = readStream.ReadToEnd();
                response.Close();
                readStream.Close();

                data = data.TrimStart(new char[] { '[' }).TrimEnd(new char[] { ']' });
                string[] split = data.Split(',');
                List<string> uvr18 = new List<string>();
                for (int i = 0; i < split.Length; i++)
                {
                    //remove{ and }
                    if (i % 4 == 0)
                        split[i] = split[i].TrimStart(new char[] { '{' });
                    else if (i % 4 == 3)
                        split[i] = split[i].TrimEnd(new char[] { '}' });
                    if (i % 4 == 0)
                    {
                        string postc = split[i].Split(':')[1].TrimStart(new char[] { ' ', '\'' }).TrimEnd(new char[] { '\'' });
                        uvr18.Add(postc);
                    }
                    else if (i % 4 == 1)
                    {
                        string subu = split[i].Split(':')[1].TrimStart(new char[] { ' ', '\'' }).TrimEnd(new char[] { '\'' });
                        uvr18.Add(subu);
                    }
                    else if (i % 4 == 2)
                    {
                        string uvrtoday = split[i].Split(':')[1].TrimStart(new char[] { ' ' });
                        uvr18.Add(uvrtoday);
                    }
                    else
                    {
                        string maxuvr = split[i].Split(':')[1].TrimStart(new char[] { ' ' });
                        uvr18.Add(maxuvr);
                    }
                }
                string pos1 = uvr18[0];
                ViewBag.pos1 = pos1;
                string sub1 = uvr18[1];
                ViewBag.sub1 = sub1;
                string uvr1 = uvr18[2];
                ViewBag.uvr1 = uvr1;
                string uvrm1 = uvr18[3];
                ViewBag.uvrm1 = uvrm1;

                string pos2 = uvr18[4];
                ViewBag.pos2 = pos2;
                string sub2 = uvr18[5];
                ViewBag.sub2 = sub2;
                string uvr2 = uvr18[6];
                ViewBag.uvr2 = uvr2;
                string uvrm2 = uvr18[7];
                ViewBag.uvrm2 = uvrm2;

                string pos3 = uvr18[8];
                ViewBag.pos3 = pos3;
                string sub3 = uvr18[9];
                ViewBag.sub3 = sub3;
                string uvr3 = uvr18[10];
                ViewBag.uvr3 = uvr3;
                string uvrm3 = uvr18[11];
                ViewBag.uvrm3 = uvrm3;

                string pos4 = uvr18[12];
                ViewBag.pos4 = pos4;
                string sub4 = uvr18[13];
                ViewBag.sub4 = sub4;
                string uvr4 = uvr18[14];
                ViewBag.uvr4 = uvr4;
                string uvrm4 = uvr18[15];
                ViewBag.uvrm4 = uvrm4;

                string pos5 = uvr18[16];
                ViewBag.pos5 = pos5;
                string sub5 = uvr18[17];
                ViewBag.sub5 = sub5;
                string uvr5 = uvr18[18];
                ViewBag.uvr5 = uvr5;
                string uvrm5 = uvr18[19];
                ViewBag.uvrm5 = uvrm5;

                string pos6 = uvr18[20];
                ViewBag.pos6 = pos6;
                string sub6 = uvr18[21];
                ViewBag.sub6 = sub6;
                string uvr6 = uvr18[22];
                ViewBag.uvr6 = uvr6;
                string uvrm6 = uvr18[23];
                ViewBag.uvrm6 = uvrm6;

                string pos7 = uvr18[24];
                ViewBag.pos7 = pos7;
                string sub7 = uvr18[25];
                ViewBag.sub7 = sub7;
                string uvr7 = uvr18[26];
                ViewBag.uvr7 = uvr7;
                string uvrm7 = uvr18[27];
                ViewBag.uvrm7 = uvrm7;

                string pos8 = uvr18[28];
                ViewBag.pos8 = pos8;
                string sub8 = uvr18[29];
                ViewBag.sub8 = sub8;
                string uvr8 = uvr18[30];
                ViewBag.uvr8 = uvr8;
                string uvrm8 = uvr18[31];
                ViewBag.uvrm8 = uvrm8;

                string pos9 = uvr18[32];
                ViewBag.pos9 = pos9;
                string sub9 = uvr18[33];
                ViewBag.sub9 = sub9;
                string uvr9 = uvr18[34];
                ViewBag.uvr9 = uvr9;
                string uvrm9 = uvr18[35];
                ViewBag.uvrm9 = uvrm9;

                string pos10 = uvr18[36];
                ViewBag.pos10 = pos10;
                string sub10 = uvr18[37];
                ViewBag.sub10 = sub10;
                string uvr10 = uvr18[38];
                ViewBag.uvr10 = uvr10;
                string uvrm10 = uvr18[39];
                ViewBag.uvrm10 = uvrm10;

                return View();
            }
            return null;

            //This version of code is for testing
            /*string data = "[{'postcode': '3000', 'suburb': 'MELBOURNE', 'UVR': 0, 'max_UVR': 4.6973}, {'postcode': '3003', 'suburb': 'WEST MELBOURNE', 'UVR': 0, 'max_UVR': 4.6973}, {'postcode': '3004', 'suburb': 'MELBOURNE', 'UVR': 0, 'max_UVR': 4.6973}, {'postcode': '3008', 'suburb': 'DOCKLANDS', 'UVR': 0, 'max_UVR': 4.6973}, {'postcode': '3010', 'suburb': 'UNIVERSITY OF MELBOURNE', 'UVR': 0, 'max_UVR': 4.6973}, {'postcode': '3050', 'suburb': 'ROYAL MELBOURNE HOSPITAL', 'UVR': 0, 'max_UVR': 4.6973}, {'postcode': '3051', 'suburb': 'HOTHAM HILL', 'UVR': 0, 'max_UVR': 4.6973}, {'postcode': '3051', 'suburb': 'HOTHAM HILL', 'UVR': 0, 'max_UVR': 4.6973}, {'postcode': '3052', 'suburb': 'MELBOURNE UNIVERSITY', 'UVR': 0, 'max_UVR': 4.6973}, {'postcode': '3052', 'suburb': 'MELBOURNE UNIVERSITY', 'UVR': 0, 'max_UVR': 4.6973}, {'postcode': '3053', 'suburb': 'CARLTON', 'UVR': 0, 'max_UVR': 4.6973}, {'postcode': '3053', 'suburb': 'CARLTON', 'UVR': 0, 'max_UVR': 4.6973}, {'postcode': '3054', 'suburb': 'CARLTON NORTH', 'UVR': 0, 'max_UVR': 4.6973}, {'postcode': '3054', 'suburb': 'CARLTON NORTH', 'UVR': 0, 'max_UVR': 4.6973}, {'postcode': '3065', 'suburb': 'FITZROY', 'UVR': 0, 'max_UVR': 4.6973}, {'postcode': '3066', 'suburb': 'COLLINGWOOD', 'UVR': 0, 'max_UVR': 4.6973}, {'postcode': '3066', 'suburb': 'COLLINGWOOD', 'UVR': 0, 'max_UVR': 4.6973}, {'postcode': '3067', 'suburb': 'ABBOTSFORD', 'UVR': 0, 'max_UVR': 4.6973}]";
            data = data.TrimStart(new char[] { '[' }).TrimEnd(new char[] { ']' });

            string[] split = data.Split(',');
            List<string> uvr18 = new List<string>();
            for (int i = 0; i < split.Length; i++)
            {
                //remove{ and }
                if (i % 4 == 0)
                    split[i] = split[i].TrimStart(new char[] { '{' });
                else if (i % 4 == 3)
                    split[i] = split[i].TrimEnd(new char[] { '}' });
                if (i % 4 == 0)
                {
                    string postc = split[i].Split(':')[1].TrimStart(new char[] { ' ', '\'' }).TrimEnd(new char[] { '\'' });
                    uvr18.Add(postc);
                }
                else if (i % 4 == 1)
                {
                    string subu = split[i].Split(':')[1].TrimStart(new char[] { ' ', '\'' }).TrimEnd(new char[] { '\'' });
                    uvr18.Add(subu);
                }
                else if (i % 4 == 2)
                {
                    string uvrtoday = split[i].Split(':')[1].TrimStart(new char[] { ' ' });
                    uvr18.Add(uvrtoday);
                }
                else
                {
                    string maxuvr = split[i].Split(':')[1].TrimStart(new char[] { ' ' });
                    uvr18.Add(maxuvr);
                }
            }
            string pos1 = uvr18[0];
            ViewBag.pos1 = pos1;
            string sub1 = uvr18[1];
            ViewBag.sub1 = sub1;
            string uvr1 = uvr18[2];
            ViewBag.uvr1 = uvr1;
            string uvrm1 = uvr18[3];
            ViewBag.uvrm1 = uvrm1;

            string pos2 = uvr18[4];
            ViewBag.pos2 = pos2;
            string sub2 = uvr18[5];
            ViewBag.sub2 = sub2;
            string uvr2 = uvr18[6];
            ViewBag.uvr2 = uvr2;
            string uvrm2 = uvr18[7];
            ViewBag.uvrm2 = uvrm2;

            string pos3 = uvr18[8];
            ViewBag.pos3 = pos3;
            string sub3 = uvr18[9];
            ViewBag.sub3 = sub3;
            string uvr3 = uvr18[10];
            ViewBag.uvr3 = uvr3;
            string uvrm3 = uvr18[11];
            ViewBag.uvrm3 = uvrm3;

            string pos4 = uvr18[12];
            ViewBag.pos4 = pos4;
            string sub4 = uvr18[13];
            ViewBag.sub4 = sub4;
            string uvr4 = uvr18[14];
            ViewBag.uvr4 = uvr4;
            string uvrm4 = uvr18[15];
            ViewBag.uvrm4 = uvrm4;

            string pos5 = uvr18[16];
            ViewBag.pos5 = pos5;
            string sub5 = uvr18[17];
            ViewBag.sub5 = sub5;
            string uvr5 = uvr18[18];
            ViewBag.uvr5 = uvr5;
            string uvrm5 = uvr18[19];
            ViewBag.uvrm5 = uvrm5;

            string pos6 = uvr18[20];
            ViewBag.pos6 = pos6;
            string sub6 = uvr18[21];
            ViewBag.sub6 = sub6;
            string uvr6 = uvr18[22];
            ViewBag.uvr6 = uvr6;
            string uvrm6 = uvr18[23];
            ViewBag.uvrm6 = uvrm6;

            string pos7 = uvr18[24];
            ViewBag.pos7 = pos7;
            string sub7 = uvr18[25];
            ViewBag.sub7= sub7;
            string uvr7 = uvr18[26];
            ViewBag.uvr7 = uvr7;
            string uvrm7 = uvr18[27];
            ViewBag.uvrm7 = uvrm7;

            string pos9 = uvr18[32];
            ViewBag.pos9 = pos9;
            string sub9 = uvr18[33];
            ViewBag.sub9 = sub9;
            string uvr9 = uvr18[34];
            ViewBag.uvr9 = uvr9;
            string uvrm9 = uvr18[35];
            ViewBag.uvrm9 = uvrm9;

            string pos11 = uvr18[40];
            ViewBag.pos11 = pos11;
            string sub11 = uvr18[41];
            ViewBag.sub11 = sub11;
            string uvr11 = uvr18[42];
            ViewBag.uvr11 = uvr11;
            string uvrm11 = uvr18[43];
            ViewBag.uvrm11 = uvrm11;

            string pos13 = uvr18[48];
            ViewBag.pos13 = pos13;
            string sub13 = uvr18[49];
            ViewBag.sub13 = sub13;
            string uvr13 = uvr18[50];
            ViewBag.uvr13 = uvr13;
            string uvrm13 = uvr18[51];
            ViewBag.uvrm13 = uvrm13;

            string pos15 = uvr18[56];
            ViewBag.pos15 = pos15;
            string sub15 = uvr18[57];
            ViewBag.sub15 = sub15;
            string uvr15 = uvr18[58];
            ViewBag.uvr15 = uvr15;
            string uvrm15 = uvr18[59];
            ViewBag.uvrm15 = uvrm15;

            string pos16 = uvr18[60];
            ViewBag.pos16 = pos16;
            string sub16 = uvr18[61];
            ViewBag.sub16 = sub16;
            string uvr16 = uvr18[62];
            ViewBag.uvr16 = uvr16;
            string uvrm16= uvr18[63];
            ViewBag.uvrm16 = uvrm16;

            string pos18 = uvr18[68];
            ViewBag.pos18 = pos18;
            string sub18 = uvr18[69];
            ViewBag.sub18 = sub18;
            string uvrr18 = uvr18[70];
            ViewBag.uvrr18 = uvrr18;
            string uvrm18 = uvr18[71];
            ViewBag.uvrm18 = uvrm18;

            return View();*/
        }

        [HttpGet]
        public ActionResult Data()
        {
            ViewBag.Title = "UV Data";
            ViewBag.su1 = "Certain Places";

            return View();
        }

        /**This part of code is for sample code**/
        /*[HttpPost]
        public ActionResult Data(string su)
        {
            ViewBag.Title = "UV Data";
            string data = "[{'postcode': '3000', 'suburb': 'MELBOURNE', 'UVR': 0, 'max_UVR': 4.6973}, {'postcode': '3003', 'suburb': 'WEST MELBOURNE', 'UVR': 0, 'max_UVR': 4.6973}, {'postcode': '3004', 'suburb': 'MELBOURNE', 'UVR': 0, 'max_UVR': 4.6973}, {'postcode': '3008', 'suburb': 'DOCKLANDS', 'UVR': 0, 'max_UVR': 4.6973}, {'postcode': '3010', 'suburb': 'UNIVERSITY OF MELBOURNE', 'UVR': 0, 'max_UVR': 4.6973}, {'postcode': '3050', 'suburb': 'ROYAL MELBOURNE HOSPITAL', 'UVR': 0, 'max_UVR': 4.6973}, {'postcode': '3051', 'suburb': 'HOTHAM HILL', 'UVR': 0, 'max_UVR': 4.6973}, {'postcode': '3051', 'suburb': 'HOTHAM HILL', 'UVR': 0, 'max_UVR': 4.6973}, {'postcode': '3052', 'suburb': 'MELBOURNE UNIVERSITY', 'UVR': 0, 'max_UVR': 4.6973}, {'postcode': '3052', 'suburb': 'MELBOURNE UNIVERSITY', 'UVR': 0, 'max_UVR': 4.6973}, {'postcode': '3053', 'suburb': 'CARLTON', 'UVR': 0, 'max_UVR': 4.6973}, {'postcode': '3053', 'suburb': 'CARLTON', 'UVR': 0, 'max_UVR': 4.6973}, {'postcode': '3054', 'suburb': 'CARLTON NORTH', 'UVR': 0, 'max_UVR': 4.6973}, {'postcode': '3054', 'suburb': 'CARLTON NORTH', 'UVR': 0, 'max_UVR': 4.6973}, {'postcode': '3065', 'suburb': 'FITZROY', 'UVR': 0, 'max_UVR': 4.6973}, {'postcode': '3066', 'suburb': 'COLLINGWOOD', 'UVR': 0, 'max_UVR': 4.6973}, {'postcode': '3066', 'suburb': 'COLLINGWOOD', 'UVR': 0, 'max_UVR': 4.6973}, {'postcode': '3067', 'suburb': 'ABBOTSFORD', 'UVR': 0, 'max_UVR': 4.6973}]";
            data = data.TrimStart(new char[] { '[' }).TrimEnd(new char[] { ']' });

            string[] split = data.Split(',');
            List<string> uvr18 = new List<string>();
            for (int i = 0; i < split.Length; i++)
            {
                //remove{ and }
                if (i % 4 == 0)
                    split[i] = split[i].TrimStart(new char[] { '{' });
                else if (i % 4 == 3)
                    split[i] = split[i].TrimEnd(new char[] { '}' });
                if (i % 4 == 0)
                {
                    string postc = split[i].Split(':')[1].TrimStart(new char[] { ' ', '\'' }).TrimEnd(new char[] { '\'' });
                    uvr18.Add(postc);
                }
                else if (i % 4 == 1)
                {
                    string subu = split[i].Split(':')[1].TrimStart(new char[] { ' ', '\'' }).TrimEnd(new char[] { '\'' });
                    uvr18.Add(subu);
                }
                else if (i % 4 == 2)
                {
                    string uvrtoday = split[i].Split(':')[1].TrimStart(new char[] { ' ' });
                    uvr18.Add(uvrtoday);
                }
                else {
                    string maxuvr = split[i].Split(':')[1].TrimStart(new char[] { ' ' });
                    uvr18.Add(maxuvr);
                }
            }

            for (int i = 0; i < uvr18.Count; i++)
            {
                if (uvr18[i].Equals(su))
                {
                    //hhh.postcode = su;
                     string aa = uvr18[i + 1];
                     string bb = uvr18[i + 2];
                     string cc = uvr18[i + 3];
                    
                    ViewBag.datauvr = bb;
                    ViewBag.datauvrmax = cc;
                    ViewBag.datasu = aa;
                }
               
            }

            //About uvr to clothes
            string data1 = "[{'type': 'hat', 'hat_type': 'Not needed', 'forehead': 0, 'cheek': 0, 'nose': 0, 'ear': 0, 'chin': 0, 'neck': 0}, {'type': 'sunglasses', 'lens_category': 0, 'function': 'Fashion spectacles', 'situation': 'Against wind, dust or debris, but not against sun', 'glare': 'not against sun'}, {'type': 'sunscreen', 'PA': 1, 'desc': 'Some UVA protection', 'SPF': 4, 'UVB_percentage': 75.0, 'situation': None}, {'type': 'umbrella_clothes', 'UPF': '0 to 10', 'UVB_percentage': '>10.1'}]";
            data1 = data1.TrimStart(new char[] { '[' }).TrimEnd(new char[] { ']' });
            string[] sepa = { ", {" };


            string hat = data1.Split(sepa, System.StringSplitOptions.RemoveEmptyEntries)[0];
            hat = hat.TrimStart(new char[] { '{' }).TrimEnd(new char[] { '}' });
            string[] hat1 = hat.Split(',');
            List<string> hat2 = new List<string>();
            for (int i = 0; i < hat1.Length; i++)
               hat2.Add(hat1[i].Split(':')[1].TrimStart(new char[] { '\'', ' ' }).TrimEnd(new char[] { '\'' }));
            string hatType = hat2[1];
            ViewBag.hat = hatType;

            string sunglasses = data1.Split(sepa, System.StringSplitOptions.RemoveEmptyEntries)[1];
            //test string 
            sunglasses = sunglasses.TrimEnd(new char[] { '}' });
            //string[] sunglasses1 = sunglasses.Split(':');
            List<string> sunglasses2 = new List<string>();
            //regular expression
            Regex regex = new Regex("\'(.*?)\'|([0-9]{1,})");
            //find match
            var matches = regex.Matches(sunglasses);
            foreach (Match match in matches)
            //  Console.WriteLine(match.Groups[0].ToString());
               sunglasses2.Add(match.Groups[0].ToString());
            string glassca = sunglasses2[3];
            ViewBag.sunglasses = glassca;

            string suncream = data1.Split(sepa, System.StringSplitOptions.RemoveEmptyEntries)[2];
            //test string 
            suncream = suncream.TrimEnd(new char[] { '}' });
            string[] suncream1 = suncream.Split(':');
            List<string> suncream2 = new List<string>();
            for (int i = 1; i < suncream1.Length; i++)
            {
               suncream2.Add(suncream1[i].Split(',')[0].TrimStart(new char[] { '\'',' ' }).TrimEnd(new char[] { '\'' }));
            }
            string spf = suncream2[3];
            string pa = suncream2[1];
            ViewBag.spf = spf;
            ViewBag.pa = pa;

            //'type': 'umbrella_clothes', 'UPF': '0 to 10', 'UVB_percentage': '>10.1'}
            string cloth = data1.Split(sepa, System.StringSplitOptions.RemoveEmptyEntries)[3];
            cloth = cloth.TrimEnd(new char[] { '}' });
            string[] cloth1 = cloth.Split(':');
            List<string> cloth2 = new List<string>();
            for (int i = 1; i < cloth1.Length; i++)
            {
                cloth2.Add(cloth1[i].Split(',')[0].TrimStart(new char[] { '\'', ' ' }).TrimEnd(new char[] { '\'' }));
            }
            string upf = cloth2[1];
            ViewBag.upf = upf;

            return View();
        }*/

        /**This part of code is for url**/
        [HttpPost]
        public ActionResult Data(string su)
        {
            ViewBag.Title = "UV Data";
           
            string uvr1 = null;
            //receive postcode from user input and show uvr information. Source codes come from: http://www.codeproject.com/Questions/204778/Get-HTML-code-from-a-website-C 
            string urlAddress = "https://lemonumbrella.azurewebsites.net/uvr_location?postcode=" + su;
            HttpWebRequest request = (HttpWebRequest)WebRequest.Create(urlAddress);
            HttpWebResponse response = (HttpWebResponse)request.GetResponse();
            if (response.StatusCode == HttpStatusCode.OK)
            {
                Stream receiveStream = response.GetResponseStream();
                StreamReader readStream = null;
                if (response.CharacterSet == null)
                    readStream = new StreamReader(receiveStream);
                else
                    readStream = new StreamReader(receiveStream, Encoding.GetEncoding(response.CharacterSet));
                string data = readStream.ReadToEnd();
                response.Close();
                readStream.Close();

                //This is what we extract sururb, UVR and max UVR
                //One data sample is: {'postcode': '123400', 'suburb': 'Default data', 'UVR': 2.3949, 'max_UVR': 13.2506}
                string[] split = data.Split(',');
                List<string> data1 = new List<string>();
                for (int i = 0; i < split.Length; i++)
                {
                    string b = split[i].Split(':')[1].TrimStart(new char[] { ' ', '\'' }).TrimEnd(new char[] { '\'', '}' });
                    data1.Add(b);
                }
                string su1 = data1[1];
                uvr1 = data1[2];
                string uvrmax1 = data1[3];
                ViewBag.su1 = su1;
                ViewBag.uvr1 = uvr1;
                ViewBag.uvrmax1 = uvrmax1;

                string urlAddress1 = "https://lemonumbrella.azurewebsites.net/uvr_protector?uvr=" + uvr1;
                ViewBag.urlAddress1 = urlAddress1;

                HttpWebRequest request1 = (HttpWebRequest)WebRequest.Create(urlAddress1);
                HttpWebResponse response1 = (HttpWebResponse)request1.GetResponse();
                if (response1.StatusCode == HttpStatusCode.OK)
                {
                    Stream receiveStream1 = response1.GetResponseStream();
                    StreamReader readStream1 = null;
                    if (response1.CharacterSet == null)
                        readStream1 = new StreamReader(receiveStream1);
                    else
                        readStream1 = new StreamReader(receiveStream1, Encoding.GetEncoding(response1.CharacterSet));
                    string dataclo = readStream1.ReadToEnd();
                    response1.Close();
                    readStream1.Close();

                    //Extract relative information for protectors
                    //1. uvr<5 or uvr>10: show 1  hat type; 2. uvr>5 and uvr<=7  4 hat types; 3. uvr>7 and uvr<=10 3 hat types

                    //replace " with \" & remove [,]
                    dataclo = dataclo.Replace("\"", "\"");
                    dataclo = dataclo.Replace("\\xa0", "");
                    dataclo = dataclo.Replace("None", "null");

                    dataclo = dataclo.TrimStart(new char[] { '[' }).TrimEnd(new char[] { ']' });
                    //it will show only one hat type
                    if (Convert.ToDouble(uvr1) <= 5 || Convert.ToDouble(uvr1) > 10)
                    {
                        List<string> data510 = new List<string>();
                        Regex regex = new Regex(@"\{(.*?)\}");
                        //find match
                        var matches = regex.Matches(dataclo);
                        foreach (Match match in matches)
                            data510.Add(match.Groups[0].ToString());
                        string hat = "";
                        string len = "";
                        string spf = "";
                        string upf = "";
                        for (int i = 0; i < 4; i++)
                        {
                            string qq = data510[i];
                            JObject json1 = JObject.Parse(qq);
                            string dd = Convert.ToString(json1["hat_type"]);
                            hat = hat + dd + "  ";

                            len = len + Convert.ToString(json1["lens_category"]);

                            spf = spf + Convert.ToString(json1["SPF"]);

                            upf = upf + Convert.ToString(json1["UPF"]);
                        }
                        ViewBag.upf = upf;
                        ViewBag.spf = spf;
                        ViewBag.len = len;
                        ViewBag.hat = hat;

                        return View();
                    }
                    //it will show 4 hat types
                    else if (Convert.ToDouble(uvr1) > 5 && Convert.ToDouble(uvr1) <= 7)
                    {
                        List<string> data57 = new List<string>();
                        Regex regex = new Regex(@"\{(.*?)\}");
                        //find match
                        var matches = regex.Matches(dataclo);
                        foreach (Match match in matches)
                            data57.Add(match.Groups[0].ToString());
                        string hat = "";
                        string len = "";
                        string spf = "";
                        string upf = "";
                        for (int i = 0; i < 7; i++)
                        {
                            string qq = data57[i];
                            JObject json1 = JObject.Parse(qq);
                            string dd = Convert.ToString(json1["hat_type"]);
                            hat = hat + dd + "  ";

                            len = len + Convert.ToString(json1["lens_category"]);

                            spf = spf + Convert.ToString(json1["SPF"]);

                            upf = upf + Convert.ToString(json1["UPF"]);
                        }
                        ViewBag.upf = upf;
                        ViewBag.spf = spf;
                        ViewBag.len = len;
                        ViewBag.hat = hat;

                        return View();
                    }
                    //it will show 3 hat types
                    else if (Convert.ToDouble(uvr1) > 7 && Convert.ToDouble(uvr1) <= 10)
                    {
                        List<string> data710 = new List<string>();
                        Regex regex = new Regex(@"\{(.*?)\}");
                        //find match
                        var matches = regex.Matches(dataclo);
                        foreach (Match match in matches)
                            data710.Add(match.Groups[0].ToString());
                        string hat = "";
                        string len = "";
                        string spf = "";
                        string upf = "";
                        for (int i = 0; i < 6; i++)
                        {
                            string qq = data710[i];
                            JObject json1 = JObject.Parse(qq);
                            string dd = Convert.ToString(json1["hat_type"]);
                            hat = hat + dd + "  ";

                            len = len + Convert.ToString(json1["lens_category"]);

                            spf = spf + Convert.ToString(json1["SPF"]);

                            upf = upf + Convert.ToString(json1["UPF"]);
                        }
                        ViewBag.upf = upf;
                        ViewBag.spf = spf;
                        ViewBag.len = len;
                        ViewBag.hat = hat;

                        return View();
                    }

                }
                return null;
            }
            return null;
        }
    }
}