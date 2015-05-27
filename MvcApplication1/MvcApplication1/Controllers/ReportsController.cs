using System;
using System.Collections.Generic;
using System.Data;
using System.Data.Entity;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using MvcApplication1.Models;

namespace MvcApplication1.Controllers
{
    public class ReportsController : Controller
    {
        private ReportDBContext db = new ReportDBContext();

        //
        // GET: /Reports/

        public ActionResult Index()
        {
            return View(db.Reports.ToList());
        }

        //
        // GET: /Reports/Details/5

        public ActionResult Details(int id = 0)
        {
            ReportDB reportdb = db.Reports.Find(id);
            if (reportdb == null)
            {
                return HttpNotFound();
            }
            return View(reportdb);
        }

        //
        // GET: /Reports/Create

        public ActionResult Create()
        {
            return View();
        }

        //
        // POST: /Reports/Create

        [HttpPost]
        [ValidateAntiForgeryToken]
        public ActionResult Create(ReportDB reportdb)
        {
            if (ModelState.IsValid)
            {
                db.Reports.Add(reportdb);
                db.SaveChanges();
                return RedirectToAction("Index");
            }

            return View(reportdb);
        }

        //
        // GET: /Reports/Edit/5

        public ActionResult Edit(int id = 0)
        {
            ReportDB reportdb = db.Reports.Find(id);
            if (reportdb == null)
            {
                return HttpNotFound();
            }
            return View(reportdb);
        }

        //
        // POST: /Reports/Edit/5

        [HttpPost]
        [ValidateAntiForgeryToken]
        public ActionResult Edit(ReportDB reportdb)
        {
            if (ModelState.IsValid)
            {
                db.Entry(reportdb).State = EntityState.Modified;
                db.SaveChanges();
                return RedirectToAction("Index");
            }
            return View(reportdb);
        }

        //
        // GET: /Reports/Delete/5

        public ActionResult Delete(int id = 0)
        {
            ReportDB reportdb = db.Reports.Find(id);
            if (reportdb == null)
            {
                return HttpNotFound();
            }
            return View(reportdb);
        }

        //
        // POST: /Reports/Delete/5

        [HttpPost, ActionName("Delete")]
        [ValidateAntiForgeryToken]
        public ActionResult DeleteConfirmed(int id)
        {
            ReportDB reportdb = db.Reports.Find(id);
            db.Reports.Remove(reportdb);
            db.SaveChanges();
            return RedirectToAction("Index");
        }

        protected override void Dispose(bool disposing)
        {
            db.Dispose();
            base.Dispose(disposing);
        }
    }
}