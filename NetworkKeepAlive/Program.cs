using System;
using System.Net;
using System.Net.NetworkInformation;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Runtime.InteropServices;
using DotRas;
using System.IO;

namespace NetworkKeepAlive {

    class Program {

        static bool isDialing = false;
        static object lockIsDialing = new object();

        static void Main(string[] args) {
            //NetworkChange.NetworkAddressChanged += new NetworkAddressChangedEventHandler(AvailabilityChangedCallback);
            RasConnectionWatcher watcher = new RasConnectionWatcher();
            watcher.Disconnected += OnConnectionDisconnected;

            //OutputStatics();
            watcher.Start();
            Console.WriteLine("Listening for PPPoE changes. Q for quit and C for a immediate dial.");
            while(true) {
                var key = Console.ReadKey();
                if (key.Key == ConsoleKey.Q) break;
                else if (key.Key == ConsoleKey.C) {
                    lock(lockIsDialing) {
                        if (isDialing) continue;
                        isDialing = true;
                    }
                    DialMyPPPoE();
                    lock (lockIsDialing) {
                        isDialing = false;
                    }
                }
            }

            watcher.Stop();
            Console.WriteLine("Goodbye~");
        }

        static void DialMyPPPoE() {
            bool isSuccess = true;
            UInt32 retryCounter = 5;

            while(retryCounter != 0) {
                try {
                    RasDialer dialer = new RasDialer();
                    dialer.EntryName = "Test";
                    dialer.PhoneBookPath = Path.Combine(
                        Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData),
                        @"Microsoft\Network\Connections\Pbk\rasphone.pbk");

                    var connection = dialer.Connect();

                    Console.WriteLine($"Connected!");
                    isSuccess = true;
                } catch (RasException re) {
                    Console.WriteLine($"Retry... ({re.ErrorCode}: {re.Message})");
                    isSuccess = false;
                }

                if (isSuccess) return;
                else retryCounter--;
            }

            Console.WriteLine($"Give up...");
        }

        static void OutputStatics() {
            Console.WriteLine(NetworkInterface.GetIsNetworkAvailable());

            NetworkInterface[] interfaces = NetworkInterface.GetAllNetworkInterfaces();
            foreach (var item in interfaces) {
                Console.WriteLine($"{item.Description}\t{Enum.GetName(typeof(OperationalStatus), item.OperationalStatus)}");
            }
        }

        static void OnConnectionDisconnected(object sender, RasConnectionEventArgs e) {
            Console.WriteLine($"[{System.DateTime.Now}] Disconnect {e.ConnectionInformation.EntryName}!");
            //OutputStatics();
            lock (lockIsDialing) {
                if (isDialing) return;
                isDialing = true;
            }
            DialMyPPPoE();
            lock (lockIsDialing) {
                isDialing = false;
            }
        }
    }
}
