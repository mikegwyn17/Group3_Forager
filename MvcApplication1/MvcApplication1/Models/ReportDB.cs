using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Data.Entity;

namespace MvcApplication1.Models
{
    public class ReportDB
    {
        public int id {get; set;}
        public string url {get; set;}
        public string parent_url {get; set;}
        public string error_type {get; set;}
    }

    public class ReportDBContext : DbContext
    {
        public DbSet<ReportDB> Reports {get; set;}
    }
}