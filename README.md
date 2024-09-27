# CLTV_Prediction
CLTV Prediction

Müşteri Yaşam Boyu Değeri (Customer Lifetime Value - CLTV), bir müşterinin bir işletme için gelecekte sağlayabileceği toplam geliri tahmin eden önemli bir metriktir. CLTV, özellikle pazarlama stratejileri, müşteri ilişkileri yönetimi ve kârlılık analizlerinde kritik bir rol oynar. İşletmeler, müşteri başına ne kadar gelir elde edeceklerini tahmin ederek, müşteri kazanma ve elde tutma stratejilerini optimize edebilirler.

# Veri Seti Hikayesi

Bir e-ticaret şirketi müşterilerini segmentlere ayırıp bu segmentlere göre pazarlama stratejileri belirlemek istiyor.

# Veriseti Hakkında 

ID: Müşteri ID'si
Year_Birth: Doğum Yılı
Education: Eğitim Düzeyi
Marital_Status: Medeni Durum
Income: Gelir
Kidhome: Evdeki Çocuk Sayısı
Teenhome: Evdeki Genç Sayısı
Dt_Customer: Müşteri Olma Tarihi
Recency: Son Alışverişten Bu Yana Geçen Gün Sayısı
MntWines: Şaraplara Harcanan Tutar
MntFruits: Meyvelere Harcanan Tutar
MntMeatProducts: Et Ürünlerine Harcanan Tutar
MntFishProducts: Balık Ürünlerine Harcanan Tutar
MntSweetProducts: Tatlılara Harcanan Tutar
MntGoldProds: Altın Ürünlerine Harcanan Tutar
NumDealsPurchases: İndirimli Satın Alma Sayısı
NumWebPurchases: İnternet Üzerinden Satın Alma Sayısı
NumCatalogPurchases: Katalog Üzerinden Satın Alma Sayısı
NumStorePurchases: Mağaza Üzerinden Satın Alma Sayısı
NumWebVisitsMonth: Aylık Web Ziyareti Sayısı
AcceptedCmp3: 3. Kampanya Kabul Edildi mi?
AcceptedCmp4: 4. Kampanya Kabul Edildi mi?
AcceptedCmp5: 5. Kampanya Kabul Edildi mi?
AcceptedCmp1: 1. Kampanya Kabul Edildi mi?
AcceptedCmp2: 2. Kampanya Kabul Edildi mi?
Complain: Şikayet Var mı?
Z_CostContact: İletişim Maliyeti (Değişmez Sabit)
Z_Revenue: Gelir (Değişmez Sabit)
Response: Son Kampanyaya Yanıt Verildi mi?

# Projenin Aşamaları

1. Veriyi Anlama (Data Understanding)
Bu aşamada, müşteri verilerinin genel yapısını anlamak için mevcut veriyi inceleyeceğiz. Aykırı değerleri belirlemek ve verinin doğruluğunu değerlendirmek için çeşitli fonksiyonlar kullanacağız.

2. Aykırı Değer Fonksiyonları
Veri setinde yer alan aşırı veya hatalı değerleri tespit etmek için aykırı değer analiz fonksiyonları geliştireceğiz. Bu fonksiyonlar, verinin güvenilirliğini artırmak için kullanılacaktır.

3. Verinin Okunması (Reading Data)
Veri kaynaklarından gerekli verileri okuyarak bir veri çerçevesi oluşturacağız. Bu adımda, CSV dosyaları veya veritabanlarından veri yükleme işlemleri gerçekleştireceğiz.

4. Verinin İncelenmesi (Data Exploration)
Veri setinin temel özelliklerini keşfedecek ve özet istatistikler, dağılımlar ve ilişkiler hakkında bilgi edineceğiz. Bu, modelleme için gerekli öngörüleri sağlayacaktır.

5. Lifetime Veri Yapısının Hazırlanması
Müşteri yaşam döngüsü için gerekli olan verileri yapılandıracağız. Bu, müşterilerin geçmişteki alışveriş davranışlarını ve sürekliliğini yansıtacak bir veri yapısı oluşturmayı içerir.

6. BG-NBD Modelinin Kurulması
Beta-Geometric/Negative Binomial Distribution (BG-NBD) modelini kurarak müşterilerin tekrar satın alma olasılıklarını tahmin edeceğiz. Bu model, müşterilerin satın alma davranışlarını anlamamıza yardımcı olur.

7. Tahmin Sonuçlarının Değerlendirilmesi
BG-NBD modelinin tahmin sonuçlarını analiz edip modelin doğruluğunu değerlendireceğiz. Bu aşamada, modelin performansını artırmak için gerekli düzeltmeleri yapacağız.

8. GAMMA-GAMMA Modelinin Kurulması
Müşterilerin harcama miktarlarını tahmin etmek için Gamma-Gamma modelini kuracağız. Bu model, müşterilerin yaşam boyu değerini daha doğru bir şekilde tahmin etmek için kullanılır.

9. BG-NBD ve GG Modeli ile CLTV'nin Hesaplanması
Kurulan BG-NBD ve Gamma-Gamma modelleri kullanılarak müşteri yaşam boyu değerleri (CLTV) hesaplanacak. Bu, müşteri segmentlerini belirlemek için kritik bir aşamadır.

10. CLTV'ye Göre Segmentlerin Oluşturulması
Son olarak, hesaplanan CLTV değerlerine göre müşteri segmentleri oluşturulacak. Bu segmentler, pazarlama stratejileri geliştirmek ve müşteri sadakatini artırmak için kullanılacaktır.
