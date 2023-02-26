from django.core.management.base import BaseCommand
from admin_website.models import *
from phonenumber_field.phonenumber import PhoneNumber


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('number', type=int, help='how many sessions generate')

    def handle(self, *args, **options):
        if not MainPage.objects.exists():
            main_page = MainPage.objects.create(
                image1='static_kit/website/main_page/1.jpg',
                image2='static_kit/website/main_page/2.jpg',
                image3='static_kit/website/main_page/3.jpg',
                text='Жилой комплекс «NORD» расположен  на берегу Черного моря в живописном районе Одессы. '
                     'Оригинальная архитектура комплекса делает его уникальным объектом не только для Одессы, '
                     'но и для всей Украины – дом прекрасно вписывается в архитектуру берега и открывает свои жильцам '
                     'и гостям прекрасный вид на бескрайнее море. Ярким преимуществом жилого комплекса является его '
                     'месторасположения – удобная транспортная развязка, социальная инфраструктура, парк и прекрасный '
                     'морской воздух создают все условия для комфортного проживания.',
                title='Дом24',
                show_app_urls=True,
                seo=Seo.objects.create(title='Главная страница',
                                       description='Главная страница', keywords='Home24, Дом24')
            )
            block_titles = ['Магазины, Банки, Школы', 'Рестораны и Кафе', 'Пляж', 'Спортивный Комплекс',
                            'Клубная Жизнь', 'Удобная транспортная развязка']
            block_descriptions = ['Район расположения жилого комплекса имеет всю необходимую для проживания '
                                  'социальную инфраструктуру – в непосредственной близости находятся '
                                  'лечебно-профилактические учреждения, аптеки, магазины, отделения банков, '
                                  'частные и коммерческие детские сады, школы ',
                                  'В непосредственной близости от жилого комплекса  расположены рыбный ресторан  и '
                                  'итальянская пиццерия. Кроме того, всего в десяти минутах ходьбы от комплекса '
                                  'находятся рестораны испанской, итальянской, американской, украинской и русской '
                                  'кухни, пиццерии, кафе и лаунж-бары на любой вкус. ',
                                  'Жилой комплекс расположен на берегу Черного моря в районе Аркадия. В десяти '
                                  'минутах ходьбы от него находится знаменитые пляжи Аркадия и Чайка, а чуть дальше – '
                                  'пляжи курортный, 13-ая станция Большого Фонтана, Пляжник и другие знаменитые пляжи '
                                  'Одессы!',
                                  'Всего в 5 минутах ходьбы от жилого комплекса  находится Спортивный комплекс '
                                  'Международного гуманитарного университета - это современный оборудованный комплекс '
                                  'с залами для проведения волейбольных соревнований, соревнований по танцам и борьбе '
                                  'и других спортивных мероприятий!',
                                  'Район расположения жилого комплекса  Аркадия является культовым местом ночного '
                                  'отдыха и развлечения – буквально в 5-10 минутах ходьбы от комплекса находятся '
                                  'такие места сосредоточения клубной жизни страны!',
                                  'ЖК  расположена на берегу Черного моря в районе Аркадии и имеет удобную '
                                  'транспортную развязку, позволяющую даже в час Пик быстро и без проблем доехать в '
                                  'течение десяти минут до центра города или выехать на автострады Одесской обл!']
            for index, (title, description) in enumerate(zip(block_titles, block_descriptions)):
                Block.objects.create(title=title, description=description, main_page=main_page,
                                     image=f'static_kit/website/main_page/blocks/{index + 1}.jpg')
        if not ContactPage.objects.exists():
            ContactPage.objects.create(
                title='AVADA-MEDIA',
                phone=PhoneNumber.from_string('+38 (073) 242-58-82', region="UA"),
                text='<p>Разработчиком системы&nbsp;<i><strong>"Мой Дом 24"</strong></i> является компания<strong> '
                     'AVADA-MEDIA </strong>- компания специализирующаяся на разработке web и мобильных приложений '
                     'разного уровня сложности, но неизменно высокого качества&nbsp;</p><p><i><strong>Официальный '
                     'сайт компании -&nbsp;</strong></i><a '
                     'href="https://avada-media.ua/">https://avada-media.ua/</a></p>',
                site_url='https://avada-media.ua/moydom24/',
                full_name='AVADA-MEDIA',
                location='ул. Космонавтов, 32',
                address='Малиновский р-н, г. Одесса',
                email='info@avada-media.com.ua',
                map_code='<div class="map"><iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2749'
                         '.8611266486014!2d30.713265815873395!3d46.43163207638925!2m3!1f0!2f0!3f0!3m2!1i1024!2i768'
                         '!4f13.1!3m3!1m2!1s0x40c633a651e3fd09%3A0x9331380952bbfd2c'
                         '!2z0LLRg9C70LjRhtGPINCa0L7RgdC80L7QvdCw0LLRgtGW0LIsIDMyLCDQntC00LXRgdCwLCDQntC00LXRgdGM0L'
                         'rQsCDQvtCx0LvQsNGB0YLRjCwgNjUwMDA!5e0!3m2!1suk!2sua!4v1524221669656" width="100%" '
                         'height="800" frameborder="0" style="border:0" allowfullscreen></iframe></div>',
                seo=Seo.objects.create(title='Контакты',
                                       description='Контакты', keywords='Home24, Дом24, Контакты')
            )
        if not ServicePage.objects.exists():
            service_page = ServicePage.objects.create(seo=Seo.objects.create(title='Услуги',
                                                                             description='Услуги',
                                                                             keywords='Home24, Дом24, Услуги'))
            service_texts = ['<p>Уборка и поддержание порядка на территории жилого комплекса, включая уборку '
                             'лестничных клеток, подъездов и внутренних дворов.</p><ul><li>Регулярная уборка '
                             'внутренних дворов и придомовых территорий жилого комплекса.</li><li>Очистка мусорных '
                             'контейнеров и территорий возле них.</li><li>Уборка лестничных клеток и подъездов зданий, '
                             'включая мойку стен и полов, уборку мусора, пыли и посторонних '
                             'предметов.</li><li>Поддержание порядка и чистоты на общественных территориях, '
                             'включая парковки, детские площадки, скамейки, фонтаны и т.д.</li></ul>',
                             '<p>Обслуживание системы кондиционирования и вентиляции в жилых квартирах, включая '
                             'регулярную чистку фильтров и проведение необходимого технического '
                             'обслуживания.</p><ul><li>Регулярная проверка и обслуживание систем кондиционирования '
                             'воздуха и вентиляции в жилых квартирах.</li><li>Проведение необходимых технических работ '
                             'по обслуживанию систем кондиционирования и вентиляции в жилых '
                             'квартирах.</li><li>Регулярная замена и чистка фильтров систем кондиционирования и '
                             'вентиляции в жилых квартирах.</li><li>Круглосуточное оперативное реагирование на '
                             'возможные поломки и сбои в работе систем кондиционирования и вентиляции в жилых '
                             'квартирах.</li></ul>',
                             '<p>Обслуживание парковки, включая поддержание функционирования инженерных сетей, '
                             'системы выезда-въезда и пропускного режима, а также охрану и обеспечение безопасности '
                             'жильцов и автомобилей на парковке.</p><ul><li>Регулярная проверка и обслуживание '
                             'инженерных сетей паркинга.</li><li>Поддержание работоспособности системы выезда-въезда '
                             'на парковку и системы пропускного режима для въезда на территорию '
                             'парковки.</li><li>Организация и осуществление системы охраны и обеспечения безопасности '
                             'жильцов и автомобилей на парковке.</li><li>Установка и обслуживание систем видео '
                             'наблюдения, контроля доступа и сигнализации на парковке.</li></ul>']
            service_titles = ['Уборка территории',
                              'Обслуживание системы кондиционирования и вентиляции',
                              'Обслуживание парковки']
            for index, (service_text, service_title) in enumerate(zip(service_texts,service_titles)):
                ServiceBlock.objects.create(
                    image=f'static_kit/website/contact_page/blocks/{index + 1}.jpg',
                    title=service_title,
                    text=service_text,
                    service_page=service_page,

                )
        if not TariffPage.objects.exists():
            tariff_page = TariffPage.objects.create(
                title='Тарифы',
                text='Тарифы',
                seo=Seo.objects.create(title='Тарифы', description='Тарифы', keywords='Home24, Дом24, Тарифы'))

            for index in range(3):
                TariffBlock.objects.create(
                    image=f'static_kit/website/tariff_page/blocks/{index + 1}.jpg',
                    title='Тариф',
                    tariff_page=tariff_page
                )
        if not AboutPage.objects.exists():
            about_page = AboutPage.objects.create(
                title='О управляющей компании',
                text='<p></p><p><b><i><u></u></i></b><b></b>К<i></i><b>омп</b><b><i></i><i></i></b>ания-застройщик не '
                     'тольк<i></i>о со<b></b>здала этот объект для своих покупателей, но и после окончания '
                     'строительства взяла на себя все услуги по обеспечению удобного проживания своих жильцов. Для '
                     'этого была организована управляющая компания «Морская симфония», которая осуществляет '
                     'комплексное обслуживание коммунальной сферы жизнедеятельности своих '
                     'клиентов.<br></p><p><i>Миссией управляющей компании является такая схема взаимодействия с '
                     'жильцами дома, при которой услуги компании не отвлекают их от проживания и отдыха и создают '
                     'максимально комфортную экосистему в доме. Незаметный сервис и максимально эффективная работа '
                     'являются визитной карточкой компании.</i></p><p><br>В функции управляющей компании входят как '
                     'содержание и управление хозяйством комплекса, так и охраняемой придомовой территории – уборка, '
                     'техническое обслуживание лифтового хозяйства, системы электро и водоснабжения дома, котельной и '
                     'пожарной систем, диспетчеризация, охрана, содержание придомовой территории и многое другое. В '
                     'штате компании собраны только профессионалы своего дела, которые помогут жильцам в самых '
                     'трудных и критических ситуациях решить их жилищно-коммунальные проблемы семь дней в неделю '
                     'круглосуточно – электрики и сантехники, инженеры, монтеры и другие специалисты имеют '
                     'многолетний опыт и высокий уровень квалификации. </p><p>Все это делает жилой комплекс&nbsp; '
                     'уникальным, комфортным и безопасным местом для проживания и отдыха всей семьи круглый год. '
                     'Доверьте заботу о вашем доме и вашей квартире управляющей компании&nbsp; и вы сможете круглый '
                     'год наслаждаться проживанием на берегу моря и прекрасной природой Одессы.</p><b></b><br><p></p>',
                photo='static_kit/website/about_page/1.jpg',
                additional_text='<p></p><p>Главной обязанностью управляющей компании является поддержка комфортных '
                                'условий для жильцов, оперативное реагирование на их просьбы и пожелания</p><p><b>К '
                                'дополнительным услугам управляющей компании также относятся: 24-часовая охрана '
                                'придомовой территории и паркинга, уборка территории и вывоз мусора, обслуживание '
                                'пирса и пляжа. Также при желании жильцы дома могут заказать любые '
                                'строительно-ремонтные работы от штатной бригады компании</b></p><p></p>',
                additional_title='О управляющей компании',
                seo=Seo.objects.create(title='О нас', description='О нас', keywords='Home24, Дом24, О нас')
            )
            for index in range(3):
                Document.objects.create(
                    about_page=about_page,
                    file=f'static_kit/website/about_page/documents/{index + 1}.jpg',
                    title=f'photo {index}'
                )
                Gallery.objects.create(
                    about_page=about_page,
                    image=f'static_kit/website/about_page/gallery/{index + 1}.jpg'
                )
                AdditionalGallery.objects.create(
                    about_page=about_page,
                    image=f'static_kit/website/about_page/additional_gallery/{index + 1}.jpg'
                )