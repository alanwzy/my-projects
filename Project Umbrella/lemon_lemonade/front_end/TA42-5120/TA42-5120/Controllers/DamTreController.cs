using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Web;
using System.Web.Mvc;

namespace TA42_5120.Controllers
{
    public class DamTreController : Controller
    {
        public ActionResult DamTre()
        {
            ViewBag.Title = "Damage and Treament";
            return View();
        }

        public ActionResult NewSkinDmg()
        {
            ViewBag.Title = "Damage to skin";
            return View();
        }

        public ActionResult Eyedamage()
        {
            ViewBag.Title = "Damage to eyes";
            return View();
        }

        public ActionResult Skindamage()
        {
            ViewBag.Title = "Sunburn damage";
            return View();
        }

        [HttpPost]
        public ActionResult Treatment(string aaa)
        {
            ViewBag.Title = "Sunburn's treatment";
            string urlAddress = "https://lemonumbrella.azurewebsites.net/nearby_hospitals_i2?postcode=" + aaa;
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
                ViewBag.Markers = data;

                return PartialView("Treatment");
            }
            return null;
        }

        [HttpGet]
        public ActionResult Treatment()
        {
            ViewBag.Title = "Sunburn's treatment";
            return View();
        }
    }
}