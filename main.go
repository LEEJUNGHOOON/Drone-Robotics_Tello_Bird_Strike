package main

import (
	"log"
	"net"
	"os/exec"
	"time"

	"gobot.io/x/gobot"
	"gobot.io/x/gobot/platforms/dji/tello"
)

func main() {
	drone := tello.NewDriver("8888")
	// Listening
	pc, err := net.ListenPacket("udp4", ":7532")
	if err != nil {
		log.Fatal(err)
	}
	defer pc.Close()
	// Setup for sending
	addr, err := net.ResolveUDPAddr("udp4", "192.168.10.255:11111")
	if err != nil {
		log.Fatal(err)
	}
	chunk := make([]byte, 40*1024)

	ffmpeg := exec.Command("ffmpeg", "-i", "-", "-acodec", "copy", "-vcodec", "copy")
	ffmpegIn, _ := ffmpeg.StdinPipe()
	ffmpegOut, _ := ffmpeg.StdoutPipe()
	if err := ffmpeg.Start(); err != nil {
		log.Println(err)
		return
	}

	work := func() {
		drone.On(tello.ConnectedEvent, func(data interface{}) {
			log.Println("Connected")
			drone.StartVideo()
			drone.SetVideoEncoderRate(4)
			gobot.Every(100*time.Millisecond, func() {
				drone.StartVideo()
			})
			//drone.TakeOff()
			// gobot.Every(time.Second * 5, func() {
			// 	drone.Clockwise(50)
			// 	drone.Forward(21)
			// })
		})

		drone.On(tello.VideoFrameEvent, func(data interface{}) {
			pkt := data.([]byte)
			if _, err := ffmpegIn.Write(pkt); err != nil {
				log.Println(err)
			}
			n, err := ffmpegOut.Read(chunk)
			log.Printf("Read %d bytes\n", n)

			if n > 0 {
				validData := chunk[:n]
				_, err = pc.WriteTo(validData, addr)
				if err != nil {
					log.Fatal(err)
				}
			}
		})
	}

	robot := gobot.NewRobot("tello",
		[]gobot.Connection{},
		[]gobot.Device{drone},
		work,
	)

	robot.Start()
}
