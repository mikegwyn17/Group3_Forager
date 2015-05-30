using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net;
using System.IO;
using HtmlAgilityPack;

namespace webCrawler
{
    class Program
    {
        static void Main(string[] args)
        {
            HttpWebResponse response = default(HttpWebResponse);
            HttpWebRequest request = default(HttpWebRequest);
            string current_page = "";
            string domain = "spsu.edu/";
            string start_page = "https://" + domain;
            List<string> to_search = new List<string>();
            List<string> searched = new List<string>();
            List<string> parents = new List<string>();
            string puppies = "";
            string href = "";
            to_search.Add(start_page);
            while (to_search.Count() != 0)
            {
                current_page = to_search.ElementAt(0);
                to_search.RemoveAt(0);
                if (parents.Count() != 0)
                {
                    parents.RemoveAt(0);
                }
                foreach (string link in searched)
                {
                    if (link == current_page)
                    {
                        continue;
                    }
                }
                // parse dat html
                HtmlWeb html_web = new HtmlAgilityPack.HtmlWeb();
                HtmlDocument doc = html_web.Load(current_page);
                try
                {
                    response = (HttpWebResponse)request.GetResponse();
                    Console.WriteLine(response.StatusCode);
                }
                catch (Exception ex)
                {
                    Console.WriteLine(ex.Message);
                }
                
                searched.Add(current_page);
                foreach (HtmlNode link in doc.DocumentNode.SelectNodes("//a[@href]"))
                {
                    HtmlAttribute att = link.Attributes["href"];
                    href = att.Value;
                    if (href == null)
                        break;
                    else if (href == "")
                        break;
                    else if (href.Contains("mailto:"))
                        break;
                    else if (href.ElementAt(0) == '/')
                        puppies = start_page + href;
                    else if (href.ElementAt(0) == '?')
                        puppies = start_page + href;
                    else if (href.ElementAt(0) == '#')
                        break;
                    else if (href.Contains("http"))
                        puppies = href;
                    else if (href.Contains("javascript"))
                        break;
                    else puppies = start_page + href;
                    to_search.Add(puppies);
                    parents.Add(current_page);
                    Console.WriteLine(puppies);
                }
            }
        }
    }
}
