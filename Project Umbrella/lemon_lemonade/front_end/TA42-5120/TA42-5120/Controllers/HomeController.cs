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
using TA42_5120.Models;

namespace TA42_5120.Controllers
{
    public class HomeController : Controller
    {
        //subuvr hhh = new subuvr();
        public ActionResult Index()
        {
            ViewBag.Title = "Home Page";
            return View();
        }

        public ActionResult FutureUV()
        {
            ViewBag.Title = "Future UV";
            return View();
        }

        public ActionResult ProSport()
        {
            ViewBag.Title = "Sports advice";
            return View();
        }

        public ActionResult Education()
        {
            ViewBag.Title = "Quiz";

            string urlAddress = "https://lemonumbrella.azurewebsites.net/quiz_i2";
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
                string quiz = readStream.ReadToEnd();
                response.Close();
                readStream.Close();

                quiz = quiz.TrimStart(new char[] { '[' }).TrimEnd(new char[] { ']' });
                quiz = quiz.Replace("\"","\"");
                quiz = quiz.Replace("\\n", " ");
                //Regex to extract every question
                List<string> question = new List<string>();
                //regular expression
                Regex regex = new Regex(@"\{(.*?)\}");
                //find match
                var matches = regex.Matches(quiz);
                foreach (Match match in matches)
                    question.Add(match.Groups[0].ToString());

                //question for eye damage
                string eyedamage = question[0];
                JObject json1 = JObject.Parse(eyedamage);
                string topic1 = Convert.ToString(json1["topic"]);
                if (topic1 == "Eye_dmg")
                {
                    topic1 = "Eye damage";
                }
                string question1 = "1. " + Convert.ToString(json1["question"]);
                string answer1 = Convert.ToString(json1["answer"]);
                string explanation1 = Convert.ToString(json1["explanation"]);
                string selection11 = Convert.ToString(json1["selection_1"]);
                string selection12 = Convert.ToString(json1["selection_2"]);
                ViewBag.topic1 = topic1;
                ViewBag.question1 = question1;
                ViewBag.answer1 = answer1;
                ViewBag.explanation1 = explanation1;
                ViewBag.selection11 = selection11;
                ViewBag.selection12 = selection12;

                //question for skin damage
                string skindamage = question[1];
                JObject json2 = JObject.Parse(skindamage);
                string topic2 = Convert.ToString(json2["topic"]);
                if (topic2 == "Skin_dmg")
                {
                    topic2 = "Skin damage";
                }
                string question2 = "2. " + Convert.ToString(json2["question"]);
                string answer2 = Convert.ToString(json2["answer"]);
                string explanation2 = Convert.ToString(json2["explanation"]);
                string selection21 = Convert.ToString(json2["selection_1"]);
                string selection22 = Convert.ToString(json2["selection_2"]);
                ViewBag.topic2 = topic2;
                ViewBag.question2 = question2;
                ViewBag.answer2 = answer2;
                ViewBag.explanation2 = explanation2;
                ViewBag.selection21 = selection21;
                ViewBag.selection22 = selection22;

                //question for sunscreen
                string sunscreen = question[2];
                JObject json3 = JObject.Parse(sunscreen);
                string topic3 = Convert.ToString(json3["topic"]);
                string question3 = "3. " + Convert.ToString(json3["question"]);
                string answer3 = Convert.ToString(json3["answer"]);
                string explanation3 = Convert.ToString(json3["explanation"]);
                string selection31 =  Convert.ToString(json3["selection_1"]);
                string selection32 = Convert.ToString(json3["selection_2"]);
                ViewBag.topic3 = topic3;
                ViewBag.question3 = question3;
                ViewBag.answer3 = answer3;
                ViewBag.explanation3 = explanation3;
                ViewBag.selection31 = selection31;
                ViewBag.selection32 = selection32;

                //question for sunglasses
                string sunglasses = question[3];
                JObject json4 = JObject.Parse(sunglasses);
                string topic4 = Convert.ToString(json4["topic"]);
                string question4 = "4. " +Convert.ToString(json4["question"]);
                string answer4 = Convert.ToString(json4["answer"]);
                string explanation4 = Convert.ToString(json4["explanation"]);
                string selection41 = Convert.ToString(json4["selection_1"]);
                string selection42 = Convert.ToString(json4["selection_2"]);
                ViewBag.topic4 = topic4;
                ViewBag.question4 = question4;
                ViewBag.answer4 = answer4;
                ViewBag.explanation4 = explanation4;
                ViewBag.selection41 = selection41;
                ViewBag.selection42 = selection42;

                //question for hat
                string hat = question[4];
                JObject json5 = JObject.Parse(hat);
                string topic5 = Convert.ToString(json5["topic"]);
                string question5 = "5. "+Convert.ToString(json5["question"]);
                string answer5 = Convert.ToString(json5["answer"]);
                string explanation5 = Convert.ToString(json5["explanation"]);
                string selection51 = Convert.ToString(json5["selection_1"]);
                string selection52 = Convert.ToString(json5["selection_2"]);
                ViewBag.topic5 = topic5;
                ViewBag.question5 = question5;
                ViewBag.answer5 = answer5;
                ViewBag.explanation5 = explanation5;
                ViewBag.selection51 = selection51;
                ViewBag.selection52 = selection52;

                //question for cloth
                string cloth = question[5];
                JObject json6 = JObject.Parse(cloth);
                string topic6 = Convert.ToString(json6["topic"]);
                string question6 = "6. "+ Convert.ToString(json6["question"]);
                string answer6 = Convert.ToString(json6["answer"]);
                string explanation6 = Convert.ToString(json6["explanation"]);
                string selection61 = Convert.ToString(json6["selection_1"]);
                string selection62 = Convert.ToString(json6["selection_2"]);
                ViewBag.topic6 = topic6;
                ViewBag.question6 = question6;
                ViewBag.answer6 = answer6;
                ViewBag.explanation6 = explanation6;
                ViewBag.selection61 = selection61;
                ViewBag.selection62 = selection62;

                //question for UVR
                string uvrQ = question[6];
                JObject json7 = JObject.Parse(uvrQ);
                string topic7 = Convert.ToString(json7["topic"]);
                string question7 = "7. " + Convert.ToString(json7["question"]);
                string answer7 = Convert.ToString(json7["answer"]);
                string explanation7 = Convert.ToString(json7["explanation"]);
                string selection71 = Convert.ToString(json7["selection_1"]);
                string selection72 = Convert.ToString(json7["selection_2"]);
                ViewBag.topic7 = topic7;
                ViewBag.question7 = question7;
                ViewBag.answer7 = answer7;
                ViewBag.explanation7 = explanation7;
                ViewBag.selection71 = selection71;
                ViewBag.selection72 = selection72;

                return View();
            }
            return null;
        }
    }
}