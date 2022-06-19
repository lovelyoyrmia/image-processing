from modules.sendEmail import SendEmail
import base64


class Navigation:
    def __init__(self, st):
        self.st = st

    def welcome(self):
        # self.st.image("assets/logo.png", width=200)
        # video_demo = open('assets/video_app.mp4', 'rb')
        # self.st.video(video_demo)
        self.st.markdown('''
        <video controls autoplay="true" loop="true" style="width: 100%;">
            <source src="https://siasky.net/AACnj3EkYfq0ttbxctKUUepGYsMuG2-eXKpCLmqy24Wpiw" type="video/mp4" />
        </video>
        ''', unsafe_allow_html=True)
        # self.st.markdown(
        #     """
        # ### Web Application that shows different image processing algorithms such as
        # - Gray Scale
        # - Contrast
        # - Blurring
        # - Brightness
        # - Thresholding
        # - Hue and Saturation
        # - Cartoonize Image
        # - Remove Background

        # ### Also this website has Computer Vision Features such as
        # - Face Detection
        # - Smile Detection
        # - Body and Object Detection
        # - Mask R-CNN Image
        # """
        # )

    def aboutPage(self):
        self.st.markdown(
            """
            ### Follow me on

            <link
                rel="stylesheet"
                href="https://use.fontawesome.com/releases/v5.15.4/css/all.css"
                integrity="sha384-DyZ88mC6Up2uqS4h/KRgHuoeGwBcD4Ng9SiP4dIRy0EXTlnuz47vAwmeGwVChigm"
                crossorigin="anonymous"
            />
            
            <div class='icon-container'>
                <a href='https://github.com/lovelyoyrmia' target='_blank' rel='noopener noreferrer'><i class='fab fa-github'></i></a>
                <a href='https://www.instagram.com/lovelyoyrmia/' target='_blank' rel='noopener noreferrer'><i class='fab fa-instagram'></i></a>
                <a href='https://www.linkedin.com/in/lovelyoyrmia' target='_blank' rel='noopener noreferrer'><i class='fab fa-linkedin'></i></a>
            </div>
            <div class='link-web'>
                For more info you can click here <a href='https://lovelyoyrmia.github.io' target='_blank' rel='noopener noreferrer'>My Portfolio</a>
            </div>
            <h5>Created with ❤ by Lovelyo Yeremia</h5>

            <style>
            .icon-container a {
                text-decoration: none;
                color: rgb(255, 255, 255);
                font-size: 2rem;
            }
            .link-web {
                font-size: 25px;
                font-weight: 600;
            }
            .link-web a {
                color: rgba(0, 0, 255, 0.5);
                text-decoration: none;
            }
            .icon-container {
                display: flex;
                width: 30%;
                justify-content: space-between;
            }
            .link-web a:hover,
            .icon-cotainer a:hover {
                color: rgba(255, 255, 255, 0.7);
            }
            h5 {
                margin-top: 10px;
            }
            </style>
        """,
            unsafe_allow_html=True,
        )

    def contact(self):
        self.st.subheader("Let's get in touch !")
        self.st.markdown(
            """
        |**Email**           |  **No Smartphone**| **Address**|
        |:-------------------------:|:-------------------------:|:-------------------------:|
        |mokalulovelyo@gmail.com |  +6285813501033 | Cawang, Jakarta, Indonesia |

        <div class="contact-maps">
            <iframe
                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3966.0808984882456!2d106.8623502144936!3d-6.25307156296422!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x2e69f30887bbb7ed%3A0x87e2cd019c1ed0b8!2sJl.%20Dewi%20Sartika%2C%20Kota%20Jakarta%20Timur%2C%20Daerah%20Khusus%20Ibukota%20Jakarta!5e0!3m2!1sid!2sid!4v1642613554404!5m2!1sid!2sid"
                width="600"
                height="450"
                style="border: 0"
                allowfullscreen=""
                loading="lazy"
            ></iframe>
        </div>
        <style>
            .contact-maps iframe {
                border-radius: 30px;
                width: 80%;
                margin-top: 20px;
            }
        </style>
        """,
            unsafe_allow_html=True,
        )
