using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace TA42_5120.Controllers
{
    public class ProtectorController : Controller
    {
        public ActionResult Sunglasses()
        {
            ViewBag.Title = "Sunglasses";
            return View();
        }

        public ActionResult Protector()
        {
            ViewBag.Title = "Protector";
            return View();
        }

        public ActionResult Suncream()
        {
            ViewBag.Title = "Suncream";
            return View();
        }

        public ActionResult Cloth()
        {
            ViewBag.Title = "Cloth";
            return View();
        }

        public ActionResult Hat()
        {
            ViewBag.Title = "Hat";
            return View();
        }
    }
}