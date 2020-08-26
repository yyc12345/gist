using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Runtime.InteropServices;

namespace DecompSpiritTrail {
    class Program {

        static void Main(string[] args) {
            Console.WriteLine("Decompress Spirit Trail Rec");
            try {
                if (!File.Exists(args[0]))
                    throw new Exception("fuck");
            } catch {
                Console.WriteLine("No specific rec file");
                Environment.Exit(1);
            }

            var ms = new MemoryStream();
            var fs = new FileStream(args[0], FileMode.Open, FileAccess.Read, FileShare.None);

            Console.WriteLine("zlib statics:");
            Int32 originSize = 0;
            ReadInt32(fs, ref originSize);
            Console.WriteLine($"No compressed size: {originSize}");

            var zo = new zlib.ZOutputStream(ms);
            int len;
            var data = new byte[1024];
            while ((len = fs.Read(data, 0, 1024)) > 0) {
                zo.Write(data, 0, len);
            }
            zo.finish();
            fs.Close();

            ms.Seek(0, SeekOrigin.Begin);
            Console.WriteLine($"Stream size: {ms.Length}");
            //========================================================================
            float srscore = 0f;
            Int32 hsscore = 0, statesCount = 0, trafoCount = 0;

            ReadInt32(ms, ref hsscore);
            ReadFloat(ms, ref srscore);
            ReadInt32(ms, ref statesCount);
            ReadInt32(ms, ref trafoCount);

            Console.WriteLine("file header:");
            Console.WriteLine($"HS: {hsscore}");
            Console.WriteLine($"SR: {srscore}");
            Console.WriteLine($"States block count: {statesCount}");
            Console.WriteLine($"Trafo block count: {trafoCount}");

            zo.Close();
            Console.ReadKey();
        }

        static void ReadInt32(Stream fs, ref Int32 num) {
            var data = new byte[4];
            fs.Read(data, 0, 4);
            num = BitConverter.ToInt32(data, 0);
        }

        static void ReadFloat(Stream fs, ref float num) {
            var data = new byte[4];
            fs.Read(data, 0, 4);
            num = BitConverter.ToSingle(data, 0);
        }

    }
}
