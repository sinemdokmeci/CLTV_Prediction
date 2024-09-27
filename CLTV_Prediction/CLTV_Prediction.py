##############################################################
# BG-NBD ve Gamma-Gamma ile CLTV Prediction
##############################################################

# 1. Verinin Hazırlanması (Data Preperation)
# 2. BG-NBD Modeli ile Expected Number of Transaction
# 3. Gamma-Gamma Modeli ile Expected Average Profit
# 4. BG-NBD ve Gamma-Gamma Modeli ile CLTV'nin Hesaplanması
# 5. CLTV'ye Göre Segmentlerin Oluşturulması
# 6. Çalışmanın fonksiyonlaştırılması

##############################################################
# 1. Verinin Hazırlanması (Data Preperation)
##############################################################

# Bir e-ticaret şirketi müşterilerini segmentlere ayırıp bu segmentlere göre
# pazarlama stratejileri belirlemek istiyor.

# Veri Seti Hikayesi
#https://www.kaggle.com/code/duyaryigit/rfm-segmentation-and-cltv-prediction/notebook

# Değişkenler

# ID: Müşteri ID'si
# Year_Birth: Doğum Yılı
# Education: Eğitim Düzeyi
# Marital_Status: Medeni Durum
# Income: Gelir
# Kidhome: Evdeki Çocuk Sayısı
# Teenhome: Evdeki Genç Sayısı
# Dt_Customer: Müşteri Olma Tarihi
# Recency: Son Alışverişten Bu Yana Geçen Gün Sayısı
# MntWines: Şaraplara Harcanan Tutar
# MntFruits: Meyvelere Harcanan Tutar
# MntMeatProducts: Et Ürünlerine Harcanan Tutar
# MntFishProducts: Balık Ürünlerine Harcanan Tutar
# MntSweetProducts: Tatlılara Harcanan Tutar
# MntGoldProds: Altın Ürünlerine Harcanan Tutar
# NumDealsPurchases: İndirimli Satın Alma Sayısı
# NumWebPurchases: İnternet Üzerinden Satın Alma Sayısı
# NumCatalogPurchases: Katalog Üzerinden Satın Alma Sayısı
# NumStorePurchases: Mağaza Üzerinden Satın Alma Sayısı
# NumWebVisitsMonth: Aylık Web Ziyareti Sayısı
# AcceptedCmp3: 3. Kampanya Kabul Edildi mi?
# AcceptedCmp4: 4. Kampanya Kabul Edildi mi?
# AcceptedCmp5: 5. Kampanya Kabul Edildi mi?
# AcceptedCmp1: 1. Kampanya Kabul Edildi mi?
# AcceptedCmp2: 2. Kampanya Kabul Edildi mi?
# Complain: Şikayet Var mı?
# Z_CostContact: İletişim Maliyeti (Değişmez Sabit)
# Z_Revenue: Gelir (Değişmez Sabit)
# Response: Son Kampanyaya Yanıt Verildi mi?


##########################
# Gerekli Kütüphane ve Fonksiyonlar
##########################

#!pip install lifetimes
import pandas as pd
import numpy as np
import datetime as dt
import lifetimes
from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter
from lifetimes.plotting import plot_period_transactions
import seaborn as sns
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.2f' % x)
pd.set_option('display.width', 500)

df = pd.read_csv("dataset/marketing_campaign.csv", sep="\t")
df_ = df.copy()
df.head()

#############
#Aykırı Değer Fonksiyonları
#############

# outlier_thresholds ve replacement_with_thresholds işlevleri, aykırı değerleri bastırmak için tanımlanır.
def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit

#Aykırı değer baskılama fonsiyonunu kullannan fonksiyon
def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    # dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit


#########################
# Verinin Okunması
#########################


df_ = pd.read_csv("dataset/marketing_campaign.csv")
df = df_.copy()
df.head()


#########################
# Verinin İncelenmesi
#########################


df.shape
df.dtypes
df.describe().T
df.isnull().sum()

#eksik (NaN) değerleri doldurmak için Income sütununun medyanını kullanalım.
df['Income'] = df['Income'].fillna(df['Income'].median())

# outlier_thresholds ve replacement_with_thresholds işlevleri, aykırı değerleri bastırmak için Kullanalım.
columns = ["MntWines", "MntFruits", "MntMeatProducts","MntFishProducts", "MntSweetProducts", "MntGoldProds", "NumDealsPurchases", "NumWebPurchases",
           "NumCatalogPurchases", "NumStorePurchases", "Income"]

for col in columns:
    replace_with_thresholds(df, col)

#Toplam müşteri değerini hesaplayalımç
df["customer_value_total"] = df["MntWines"] + df["MntFruits"] + df["MntMeatProducts"] + df["MntFishProducts"] + df["MntSweetProducts"] + df["MntGoldProds"]
#Tolam sipariş sayısını hesaplayalım.
df["order_num_total"] = df["NumDealsPurchases"] + df["NumWebPurchases"] + df["NumCatalogPurchases"] + df["NumStorePurchases"]
#Gereksiz sutunları çıkararak yeni datafarme elde edelim.
df = df[["ID", "Year_Birth", "Education", "Marital_Status", "Income", "Kidhome", "Teenhome", "Dt_Customer", "Recency", "customer_value_total", "order_num_total"]]

df.head()

#Birden fazla alışveriş yapan müşterileri filtreleyelim.
df = df[(df['order_num_total'] > 1) & (df['customer_value_total'] > 1)]

#Tarih sutununu datetime formatına çevirelim.
df["Dt_Customer"] = df["Dt_Customer"].apply(pd.to_datetime)

#########################
# Lifetime Veri Yapısının Hazırlanması
#########################

# recency: Son satın alma üzerinden geçen zaman. Haftalık. (kullanıcı özelinde)
# T: Müşterinin yaşı. Haftalık. (analiz tarihinden ne kadar süre önce ilk satın alma yapılmış)
# frequency: tekrar eden toplam satın alma sayısı (frequency>1)
# monetary: satın alma başına ortalama kazanç

cltv_df = pd.DataFrame()
#Müşteri İD'lerini ekleyelim
cltv_df["customer_id"] = df["ID"]
# Recency ( Müşteri Yaşı ) değerini oluşturalım. (Haftalık)
cltv_df["recency_cltv_weekly"] = df["Recency"] /7
# T (Müşterinin ilk satın almasından bu yana geçen süre) yi hesaplayalım. (Haftalık)
cltv_df["T"] = ((df['Dt_Customer'].max() - df['Dt_Customer']).dt.days / 7 ) + 20
# Frequency ( Satın Alma Sıklığı )
cltv_df["frequency"] = df["order_num_total"]
# Monatary ( Ortalama Harcama )
cltv_df["monetary_cltv_avg"] = df["customer_value_total"] / df["order_num_total"]
cltv_df.head()

##############################################################
# 2. BG-NBD Modelinin Kurulması
##############################################################

bgf = BetaGeoFitter(penalizer_coef=0.001)

bgf.fit(cltv_df['frequency'],
        cltv_df['recency_cltv_weekly'],
        cltv_df['T'])

# 1 hafta içinde en çok satın alma beklediğimiz 10 müşteri kimdir?
bgf.conditional_expected_number_of_purchases_up_to_time(1,
                                                        cltv_df['frequency'],
                                                        cltv_df['recency_cltv_weekly'],
                                                        cltv_df['T']).sort_values(ascending=False).head(10)

#Bütün müşteriler için 1 hafta da satın alma beklentisini bulalım.
cltv_df["expected_purc_1_week"] = bgf.predict(1,
                                              cltv_df['frequency'],
                                              cltv_df['recency_cltv_weekly'],
                                              cltv_df['T'])

# 1 ay içinde en çok satın alma beklediğimiz 10 müşteri kimdir?
bgf.predict(4,
            cltv_df['frequency'],
            cltv_df['recency_cltv_weekly'],
            cltv_df['T']).sort_values(ascending=False).head(10)

# 1 ay içerisinde bütün müşterilerin satın alma beklentisini bulalım.
cltv_df["expected_purc_1_month"] = bgf.predict(4,
                                               cltv_df['frequency'],
                                               cltv_df['recency_cltv_weekly'],
                                               cltv_df['T'])

# 1 ay içerisinde ki tüm şirket için satın alım beklentisini bulalım.
bgf.predict(4,
            cltv_df['frequency'],
            cltv_df['recency_cltv_weekly'],
            cltv_df['T']).sum()


# 3 ay içerisinde ki bütün müşterilerin satın alma beklentisini bulalım.
cltv_df["expected_purc_3_month"] = bgf.predict(4 * 3,
                                               cltv_df['frequency'],
                                               cltv_df['recency_cltv_weekly'],
                                               cltv_df['T'])

# 3 Ayda Tüm Şirketin Beklenen Satış Sayısı Nedir?
bgf.predict(4 * 3,
            cltv_df['frequency'],
            cltv_df['recency_cltv_weekly'],
            cltv_df['T']).sum()


################################################################
# Tahmin Sonuçlarının Değerlendirilmesi
################################################################

plot_period_transactions(bgf)
plt.show()

##############################################################
# 3. GAMMA-GAMMA Modelinin Kurulması
##############################################################

ggf = GammaGammaFitter(penalizer_coef=0.01)
cltv_df['frequency'] = cltv_df['frequency'].round()

# Gamma-Gamma modelini veriyle eğitelim.
ggf.fit(cltv_df['frequency'], cltv_df['monetary_cltv_avg'])

# Her bir müşteri için koşullu beklenen ortalama kârı hesaplayıp ve bu tahminlerin ilk 10 tanesini getirelim.
ggf.conditional_expected_average_profit(cltv_df['frequency'],
                                        cltv_df['monetary_cltv_avg']).head(10)

# Tüm müşteriler için hesaplanan beklenen ortalama kârları azalan sıraya göre sıralayıp ve en yüksek 10 müşteriyi getirelim.
ggf.conditional_expected_average_profit(cltv_df['frequency'],
                                        cltv_df['monetary_cltv_avg']).sort_values(ascending=False).head(10)

# Model ile müşterinin ortalama harcamasının tahmini değerini hesaplayalım.
cltv_df["exp_average_value"] = ggf.conditional_expected_average_profit(cltv_df['frequency'], cltv_df['monetary_cltv_avg'])

#expected_average_profit değerine göre sıralama
cltv_df.sort_values("exp_average_value", ascending=False).head(10)


##############################################################
# 4. BG-NBD ve GG modeli ile CLTV'nin hesaplanması.
##############################################################

# 3 aylık müşteri yaşam boyu değerini (cltv) hesaplanması
cltv = ggf.customer_lifetime_value(bgf,
                                   cltv_df['frequency'],
                                   cltv_df['recency_cltv_weekly'],
                                   cltv_df['T'],
                                   cltv_df['monetary_cltv_avg'],
                                   time=3,
                                   freq="W",
                                   discount_rate=0.01)
cltv_df["cltv"] = cltv

##############################################################
# 5. CLTV'ye Göre Segmentlerin Oluşturulması
##############################################################

cltv_df["cltv_segment"] = pd.qcut(cltv_df["cltv"], 4, labels=["D", "C", "B", "A"])
cltv_df = cltv_df.sort_values(by="cltv", ascending=False)
cltv_df.reset_index(inplace=True, drop=True)
cltv_df.head(10)


cltv_final = cltv_df
cltv_final.head()

# Müşterileri belirli segmentlere ayırarak her segmentteki müşterilerin bazı metriklerini  analiz edelim.
cltv_final[["cltv_segment", "recency_cltv_weekly","frequency","T","monetary_cltv_avg","exp_average_value"]].groupby("cltv_segment").agg(
    {"count", "mean"})

cltv_final[["cltv_segment", "cltv"]].groupby("cltv_segment").agg({"count"})


cltv_final.to_csv("cltv_prediction.csv")




