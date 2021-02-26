using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace VirtoolsNLPDecode {
    class Program {

        static readonly byte[] xorArray = new byte[0x80] {
            0x2C, 0xA8, 0x56, 0xF9, 0xBD, 0xA6, 0x8D, 0x15, 0x25, 0x38, 0x1A, 0xD4, 0x65, 0x58, 0x28, 0x37, 
            0xFA, 0x6B, 0xB5, 0xA1, 0x2C, 0x96, 0x13, 0xA2, 0xAB, 0x4F, 0xC5, 0xA1, 0x3E, 0xA7, 0x91, 0x8D, 
            0x2C, 0xDF, 0x78, 0x6D, 0x3C, 0xFC, 0x92, 0x1F, 0x1A, 0x62, 0xA7, 0x9C, 0x92, 0x29, 0x44, 0x6D, 
            0x3D, 0xA9, 0x2B, 0xE1, 0x91, 0xAD, 0x49, 0x3C, 0xE2, 0x33, 0xD2, 0x1A, 0x55, 0x92, 0xE7, 0x95, 
            0x8C, 0xDA, 0xD2, 0xCD, 0xA2, 0xCF, 0x92, 0x9A, 0xE1, 0xF9, 0x3A, 0x26, 0xFA, 0xC4, 0xA9, 0x23, 
            0xA9, 0x4D, 0x1A, 0x2C, 0x3C, 0x2A, 0xAC, 0x62, 0xA3, 0x92, 0xAC, 0x1F, 0x3E, 0xA6, 0xC9, 0xC8, 
            0x63, 0xCA, 0x52, 0xF9, 0xFB, 0x3A, 0x9C, 0x2A, 0xB2, 0x1A, 0x8D, 0x9A, 0x8C, 0x2A, 0x9C, 0x32, 
            0xAA, 0xC3, 0xA2, 0x97, 0x34, 0x92, 0xFA, 0x71, 0xBE, 0x3F, 0xAC, 0x28, 0x22, 0x9F, 0xAC, 0xE8
        };

        static void Main(string[] args) {
            Console.WriteLine("Virtools NLP Compresser / Decompress");

            string fileArgs1 = "";
            string fileArgs2 = "";
            string method = "";
            try {
                method = args[0];
                fileArgs1 = args[1];
                fileArgs2 = args[2];
                if (!File.Exists(fileArgs1))
                    throw new Exception("fuck");
            } catch {
                Console.WriteLine("Wrong argument or inexisting file.");
                Environment.Exit(1);
            }

            switch(method) {
                case "-d":
                    DecompressNLP(fileArgs1, fileArgs2);
                    break;
                case "-c":
                    CompressNLP(fileArgs1, fileArgs2);
                    break;
                default:
                    Console.WriteLine("Wrong argument.");
                    break;
            }

            Console.ReadKey();
        }

        static void DecompressNLP(string nlpFile, string decodeFile) {
            var ms = new MemoryStream();
            var fs = new FileStream(nlpFile, FileMode.Open, FileAccess.Read, FileShare.None);
            var crc32 = new Adler32();
            UInt32 gottenCrc32 = 0;

            var zo = new zlib.ZOutputStream(ms);
            long fulllen = fs.Length - 8;
            long times = fulllen / 1024;
            long remain = fulllen % 1024;
            var data = new byte[1024];
            while (times-- > 0) {
                fs.Read(data, 0, 1024);
                zo.Write(data, 0, 1024);
                gottenCrc32 = (UInt32)crc32.adler32(gottenCrc32, data, 0, 1024);
            }
            if (remain != 0) {
                fs.Read(data, 0, (int)remain);
                zo.Write(data, 0, (int)remain);
                gottenCrc32 = (UInt32)crc32.adler32(gottenCrc32, data, 0, (int)remain);
            }
            UInt32 fileExpectedLengthData = ReadUInt32(fs);
            UInt32 fileCrc32 = ReadUInt32(fs);
            Console.WriteLine($"Read file tail data: {fileExpectedLengthData}");
            Console.WriteLine($"Read expected file length: {(UInt32)(-1 - (0x0F956A82C ^ fileExpectedLengthData))}");
            Console.WriteLine($"File written CRC32: {fileCrc32}");
            Console.WriteLine($"Computed CRC32: {gottenCrc32 + 1072}");
            zo.finish();
            fs.Close();

            ms.Seek(0, SeekOrigin.Begin);
            Console.WriteLine($"Stream size: {ms.Length}");
            fs = new FileStream(decodeFile, FileMode.Create, FileAccess.Write, FileShare.None);
            int len;
            byte cache;
            int pos = 0;
            while ((len = ms.Read(data, 0, 1024)) > 0) {
                for (int i = 0; i < len; i++, pos++) {
                    cache = (byte)(data[i] ^ xorArray[pos & 0x7f]);
                    data[i] = cache;
                }
                fs.Write(data, 0, len);
            }

            fs.Close();
            zo.Close();

            Console.WriteLine("Decoded file has been written");
        }

        static void CompressNLP(string decodedFile, string nlpFile) {
            var ms = new MemoryStream();
            var fs = new FileStream(decodedFile, FileMode.Open, FileAccess.Read, FileShare.None);
            var crc32 = new Adler32();
            UInt32 gottenCrc32 = 0;
            UInt32 fileExpectedLengthData = (UInt32)(fs.Length);
            Console.WriteLine($"File size: {fileExpectedLengthData}");

            var zo = new zlib.ZOutputStream(ms, zlib.zlibConst.Z_DEFAULT_COMPRESSION);
            byte cache;
            var data = new byte[1024];
            int len;
            int pos = 0;
            while ((len = fs.Read(data, 0, 1024)) > 0) {
                for (int i = 0; i < len; i++, pos++) {
                    cache = (byte)(data[i] ^ xorArray[pos & 0x7f]);
                    data[i] = cache;
                }
                zo.Write(data, 0, len);
            }
            zo.finish();
            fs.Close();

            ms.Seek(0, SeekOrigin.Begin);
            fs = new FileStream(nlpFile, FileMode.Create, FileAccess.Write, FileShare.None);

            while ((len = ms.Read(data, 0, 1024)) > 0) {
                fs.Write(data, 0, len);
                gottenCrc32 = (UInt32)crc32.adler32(gottenCrc32, data, 0, len);
            }

            fileExpectedLengthData = (UInt32)((-(fileExpectedLengthData + 1)) ^ 0x0F956A82C);
            Console.WriteLine($"Written expected file length: {fileExpectedLengthData}");
            UInt32 writtenCrc32 = gottenCrc32 + 1072;
            Console.WriteLine($"File CRC32: {gottenCrc32}");
            Console.WriteLine($"Written CRC32: {writtenCrc32}");

            WriteUInt32(fs, fileExpectedLengthData);
            WriteUInt32(fs, writtenCrc32);

            fs.Close();
            zo.Close();

            Console.WriteLine("Encoded file has been written");
        }

        static UInt32 ReadUInt32(Stream fs) {
            var data = new byte[4];
            fs.Read(data, 0, 4);
            return BitConverter.ToUInt32(data, 0);
        }

        static void WriteUInt32(Stream fs, UInt32 num) {
            var data = BitConverter.GetBytes(num);
            fs.Write(data, 0, 4);
        }

    }
}
