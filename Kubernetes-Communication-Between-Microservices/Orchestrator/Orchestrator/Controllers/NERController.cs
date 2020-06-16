using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Cors;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace Orchestrator.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class NERController : ControllerBase
    {
        // GET: api/NER
        // this is for testing only
        [HttpGet]
        public IEnumerable<string> Get()
        {
            return new string[] { "value1", "value2" };
        }

        // POST: api/NER
        [HttpPost]
        public IActionResult Post()
        {
            try
            {
                string entities = string.Empty;
                string text = string.Empty;

                IFormFile file = HttpContext.Request.Form.Files.FirstOrDefault();

                //send file to OCR SERVICE - gets text
                using (var client = new HttpClient())
                {
                    client.BaseAddress = new Uri("http://ocr-service:80");

                    byte[] data;
                    using (var br = new BinaryReader(file.OpenReadStream()))
                        data = br.ReadBytes((int)file.OpenReadStream().Length);

                    ByteArrayContent bytes = new ByteArrayContent(data);

                    MultipartFormDataContent multiContent = new MultipartFormDataContent();

                    multiContent.Add(bytes, "file", file.FileName);

                    var result = client.PostAsync("ocr", multiContent).Result;

                    text = result.Content.ReadAsStringAsync().Result;
                }

                //send text received from OCR SERVICE to NER SERVICE - gets named entities
                using (var client = new HttpClient())
                {
                    client.BaseAddress = new Uri("http://ner-service:80");

                    StringContent stringContent = new StringContent(
                        text,
                       UnicodeEncoding.UTF8,
                       "application/text");

                    var result =  client.PostAsync("entities", stringContent).Result;

                    entities = result.Content.ReadAsStringAsync().Result;
                }

                //send final response (named entities) to client
                return Ok(entities);
            }
            catch (Exception ex)
            {
                return StatusCode(500); // 500 is generic server error
            }
        }
    }
}

