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
            string current_page = "";
            string domain = "spsu.edu";
            string start_page = "https://" + domain;
            List<string> to_search = new List<string>();
            List<string> searched = new List<string>();
            List<string> parents = new List<string>();
            string puppies = "";
            string href = "";
            string content = "";
            HttpWebRequest request = (HttpWebRequest)HttpWebRequest.Create(start_page);
            HttpWebResponse response = (HttpWebResponse)request.GetResponse();
            StreamReader stream = new StreamReader(response.GetResponseStream());
            string source_code = stream.ReadToEnd();
            HtmlDocument doc = new HtmlDocument();
            doc.OptionReadEncoding = false;
            to_search.Add(start_page);

            while (to_search.Count > 0)
            {
                current_page = to_search.ElementAt(0);
                to_search.RemoveAt(0);
                if (parents.Count() != 0)
                {
                    parents.RemoveAt(0);
                }
                foreach (string link in searched) // add things to searched
                {
                    if (link == current_page)
                    {
                        continue;
                    }
                }
                //request = (HttpWebRequest)HttpWebRequest.Create(current_page);
                //request.Method = "HEAD";
                ////response.Dispose();
                //try
                //{
                //    response = (HttpWebResponse)request.GetResponse();
                //    //request.EndGetResponse();

                //}
                //catch (System.Net.WebException ex)
                //{
                //    var status = response.StatusCode;
                //    switch(status.ToString())
                //    {
                //        case "NotFound":
                //            Console.WriteLine("Huzzah!");
                //            break;
                //    }
                //    Console.WriteLine(ex);
                //    continue;
                //}
                //var status_code = response.StatusCode;
                //Console.WriteLine(status_code.ToString());
                try
                {
                    request = (HttpWebRequest)HttpWebRequest.Create(current_page);
                    response = (HttpWebResponse)request.GetResponse();
                }
                catch (System.Net.WebException ex)
                {
                    Console.WriteLine(ex.Status);
                    continue;
                }
                var status = response.StatusCode;
                Console.WriteLine(status);
                searched.Add(current_page);
                content = response.ContentType;
                if (!(content.Contains("text/html") || content.Contains("application/xhtml+xml") || content.Contains("application/xml")))
                {
                    Console.WriteLine("Invalid Content type " + current_page);
                    continue;
                }
                //if (!current_page.Contains(domain)) //use host?
                //{
                //    Console.WriteLine("Off domain " + current_page);
                //    continue;
                //}
                if (!request.Host.Equals(domain))
                {
                    Console.WriteLine("Off domain " + current_page);
                    continue;
                }
                // start to parse html 
                stream = new StreamReader(response.GetResponseStream());
                source_code = stream.ReadToEnd();
                doc.LoadHtml(source_code);
                Console.WriteLine(current_page);
                var links = doc.DocumentNode.SelectNodes("//a[@href]");
                if (links != null)
                {
                    foreach (HtmlNode link in links)
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
                        //Console.WriteLine(puppies);
                    }
                }
                response.Close();
            }
        }
    }
}
