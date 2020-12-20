package main

import (
	"bytes"
	"io"
	"io/ioutil"
	"log"
	"mime/multipart"
	"net/http"
	"os"
	"os/exec"
	"path"
	"strings"
	"time"

	"gobot.io/x/gobot"
	"gobot.io/x/gobot/platforms/dji/tello"
)

const serverURI = "http://0.0.0.0:5000/face_detection"

func main() {
	drone := tello.NewDriver("8888")
	dir, err := ioutil.TempDir("", "")
	if err != nil {
		log.Fatal(err)
	}
	defer os.RemoveAll(dir) // clean up
	ffmpeg := exec.Command("ffmpeg", "-i", "-", "-r", "1", path.Join(dir, "output_%04d.png"))
	ffmpegIn, _ := ffmpeg.StdinPipe()
	if err := ffmpeg.Start(); err != nil {
		log.Println(err)
		return
	}

	work := func() {
		drone.On(tello.ConnectedEvent, func(data interface{}) {
			log.Println("Connected")
			drone.SetVideoEncoderRate(4)
			gobot.Every(time.Second, func() {
				drone.StartVideo()
			})
			drone.TakeOff()
			//gobot.After(time.Second*15, func() {
			//	drone.Clockwise(50)
			//	drone.Forward(21)
			//	drone.Land()
			//})
		})

		speed := 40

		gobot.Every(3*time.Second, func() {
			files, err := ioutil.ReadDir(dir)
			if err != nil {
				log.Fatal(err)
			}
			if len(files) == 0 {
				return
			}
			filePath := path.Join(dir, files[0].Name())
			log.Println(filePath)
			// image, err := ansimage.NewFromFile(filePath, color.Black, ansimage.NoDithering)
			// if err != nil {
			// 	log.Fatal(err)
			// }
			// image.Draw()
			message := getMessageByUploadingImage(filePath)
			for _, file := range files {
				os.Remove(path.Join(dir, file.Name()))
			}

			log.Println(message)

			if strings.Contains(message, "right") {
				drone.Right(speed)
				log.Println("-move")
				time.Sleep(time.Second) // wait for 1 second
			}
			if strings.Contains(message, "left") {
				drone.Left(speed)
				log.Println("-move")
				time.Sleep(time.Second)
			}
			if strings.Contains(message, "forward") {
				drone.Forward(speed)
				log.Println("-move")
				time.Sleep(time.Second)
			}
			if strings.Contains(message, "back") {
				drone.Backward(speed)
				log.Println("-move")
				time.Sleep(time.Second)
			}
			drone.Hover()

		})

		drone.On(tello.VideoFrameEvent, func(data interface{}) {
			pkt := data.([]byte)
			if _, err := ffmpegIn.Write(pkt); err != nil {
				log.Println(err)
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

func getMessageByUploadingImage(imagePath string) string {
	fieldname := "image"
	file, err := os.Open(imagePath)
	handleError(err)

	// リクエストボディのデータを受け取るio.Writerを生成する。
	body := &bytes.Buffer{}

	// データのmultipartエンコーディングを管理するmultipart.Writerを生成する。
	// ランダムなbase-16バウンダリが生成される。
	mw := multipart.NewWriter(body)

	// ファイルに使うパートを生成する。
	// ヘッダ以外はデータは書き込まれない。
	// fieldnameとfilenameの値がヘッダに含められる。
	// ファイルデータを書き込むio.Writerが返却される。
	fw, err := mw.CreateFormFile(fieldname, imagePath)

	// fwで作ったパートにファイルのデータを書き込む
	_, err = io.Copy(fw, file)
	handleError(err)

	// リクエストのContent-Typeヘッダに使う値を取得する（バウンダリを含む）
	contentType := mw.FormDataContentType()

	// 書き込みが終わったので最終のバウンダリを入れる
	err = mw.Close()
	handleError(err)

	// contentTypeとbodyを使ってリクエストを送信する
	resp, err := http.Post(serverURI, contentType, body)
	handleError(err)

	buf := new(bytes.Buffer)
	buf.ReadFrom(resp.Body)

	return buf.String()
}

func handleError(err error) {
	if err != nil {
		log.Fatal(err)
	}
}

func move(message string) {
	//drone := tello.NewDriver("8888")
	//drone.TakeOff()
}
