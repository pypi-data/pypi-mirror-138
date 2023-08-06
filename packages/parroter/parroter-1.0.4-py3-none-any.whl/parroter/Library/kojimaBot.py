import os
import random
from LibHanger.Library.uwImport import JsonImporter
from LibHanger.Library.uwImage import uwImage
from pandas import DataFrame
from parroter.Library.parroterBase import parroterBase
from parroter.Library.kojima.kojimaConfig import kojimaConfig
from parroter.Library.kojima.kojimaGlobals import *
from parroter.Library.kojima.Getter.lastNameList import gettr_lastNameList

class kojimaBot(parroterBase):
    
    """
    児嶋Botクラス
    """
            
    def __init__(self, rootPath, lang:str = parroterBase.botLang.jp) -> None:
        
        """
        コンストラクタ

        Parameters
        ----------
        rootPath : str
            ルートパス
        lang : str
            言語
        """
        
        # 基底側コンストラクタ
        super().__init__(rootPath, lang)
                
        # gvに設定情報をセット
        gv.config = self.config
        gv.kojimaConfig = self.settingConfig(rootPath)
        
        # kojima共通設定をメンバ変数にセット
        self.parroterConfig = gv.kojimaConfig
        
        # キートークン設定
        self.setKeyToken()

        # ログ出力先設定
        self.settingLogOutputPath()
        
    def appName(self):
        
        """
        アプリ名
        """

        return 'kojima'
    
    def settingConfig(self, rootPath):
        
        """
        parroter共通設定
        
        Parameters
        ----------
        rootPath : str
            ルートパス
        """
        
        # kojima.ini
        kc = kojimaConfig()
        kc.getConfig(rootPath, os.path.join(self.config.startupCfg.configFolderPath, self.appName()))

        return kc
    
    def getLastName(self, *args, **kwargs):
        
        """
        苗字リストを取得してDataFrameとして返す
        """
        
        getter = gettr_lastNameList()
        return getter.getAllData(**kwargs)
    
    def getHelloTweetText(self):
        
        """
        挨拶文を取得する
        """
        
        # 挨拶文の定型テキスト文取得
        helloTemplateText = self.getHelloTweetTemplateText()
                
        return helloTemplateText
    
    def getHelloTweetImage(self):
        
        """
        名言ツイート画像を生成する
        """
        
        # 名言ツイート画像を生成する
        return self.generateTweetImage()
    
    def getHelloTweetTemplateText(self):

        """
        挨拶定型文を取得する
        """
        
        with open(os.path.join(self.rootPath, 
                               self.parroterConfig.appListDir, 
                               self.parroterConfig.appHelloTextFileName),'r',encoding='utf-8') as f:
            helloTemplateText= f.read()
        
        return helloTemplateText
            
    def getWiseSayingTweetData(self):
        
        """
        名言ツイート文を取得する
        """
                
        # 名言ツイートjsonファイルをDataFrameに変換
        ji = JsonImporter(self.rootPathFull)
        dfWiseSaying = ji.convertToDataFrame(gv.kojimaConfig.wiseSayingJsonDir, gv.kojimaConfig.wiseSayingJsonFileName)
        targetTweetNo = []
        if len(dfWiseSaying) > 0:
            targetTweetNo = range(1, len(dfWiseSaying) + 1)
        else:
            return []

        # 名言ツイートNoログ取得
        wiseSayingTweetNoLogFilePath = os.path.join(self.rootPath, 
                                                    gv.kojimaConfig.wiseSayingTweetNoLogDir, 
                                                    gv.kojimaConfig.wiseSayingTweetNoLogFileName)
        
        # 名言ツイートNoログ出力先ディレクトリ作成
        wiseSayingTweetNoLogFolderDir = os.path.dirname(wiseSayingTweetNoLogFilePath)
        if not os.path.exists(wiseSayingTweetNoLogFolderDir):
            os.makedirs(wiseSayingTweetNoLogFolderDir, exist_ok=True)
            
        wiseSayingTweetNoLog = []
        if os.path.exists(wiseSayingTweetNoLogFilePath):
            
            # 名言ツイートログ読込
            with open(wiseSayingTweetNoLogFilePath,'r',encoding='utf-8') as f:
                wiseSayingTweetNoLog = f.read().split('\n')
        
        # 対象ツイートNo絞り込み   
        if len(wiseSayingTweetNoLog) > 0:
            
            # ツイート済NoはtargetTweetNoから除外する
            targetTweetNo = [tweetNo for tweetNo in targetTweetNo if not tweetNo in wiseSayingTweetNoLog]

            # 対象ツイートNoが取得できなかった場合は名言ツイートログファイルを初期化する
            if len(targetTweetNo) == 0:
                
                with open(wiseSayingTweetNoLogFilePath, mode='w') as f:
                    targetTweetNo = range(1, len(dfWiseSaying) + 1)
                    
        # ツイートNoをランダム選択
        tweetNo = random.choice(targetTweetNo)

        # ツイートNoを名言ツイートログに書込
        with open(wiseSayingTweetNoLogFilePath, mode='a') as f:
            f.write(str(tweetNo))
            f.write('\n')
        
        # dfWiseSayingから対象となるツイートを取得する
        return dfWiseSaying[dfWiseSaying['no'] == tweetNo]
    
    def getWiseSayingPtrnData(self, wiseSayingTweetPattern):
        
        """
        名言ツイートパターンリストを取得する
        
        Parameters
        ----------
        wiseSayingTweetPattern : str
            名言ツイートパターンNo

        """
        
        # 名言ツイートパターンリストjsonファイルをDataFrameに変換
        ji = JsonImporter(self.rootPathFull)
        dfWiseSayingPtrn = ji.convertToDataFrame(gv.kojimaConfig.wiseSayingJsonDir, gv.kojimaConfig.wiseSayingPtrnJsonFileName)
        
        # 該当する名言パターンを取得
        srWiseSayingPtrn = dfWiseSayingPtrn[dfWiseSayingPtrn['pattern'] == wiseSayingTweetPattern].iloc[0]
        
        # 名言パターンリストクラスへ値セット
        gv.kojimaConfig.wiseSayingPattern.pattern = wiseSayingTweetPattern
        gv.kojimaConfig.wiseSayingPattern.font_name = srWiseSayingPtrn['font_name']
        gv.kojimaConfig.wiseSayingPattern.say_ipX = srWiseSayingPtrn['say{}_ipX'.format(self._lang)]
        gv.kojimaConfig.wiseSayingPattern.say_ipY = srWiseSayingPtrn['say{}_ipY'.format(self._lang)]
        gv.kojimaConfig.wiseSayingPattern.say_fontSize = srWiseSayingPtrn['say{}_fontSize'.format(self._lang)]
        gv.kojimaConfig.wiseSayingPattern.say_indentYPoint = srWiseSayingPtrn['say{}_indentYPoint'.format(self._lang)]
        gv.kojimaConfig.wiseSayingPattern.say_txtHeight = srWiseSayingPtrn['say{}_txtHeight'.format(self._lang)]
        gv.kojimaConfig.wiseSayingPattern.category_ipX = srWiseSayingPtrn['category{}_ipX'.format(self._lang)]
        gv.kojimaConfig.wiseSayingPattern.category_ipY = srWiseSayingPtrn['category{}_ipY'.format(self._lang)]
        gv.kojimaConfig.wiseSayingPattern.category_fontSize = srWiseSayingPtrn['category{}_fontSize'.format(self._lang)]
        gv.kojimaConfig.wiseSayingPattern.category_indentYPoint = srWiseSayingPtrn['category{}_indentYPoint'.format(self._lang)]
        gv.kojimaConfig.wiseSayingPattern.category_txtHeight = srWiseSayingPtrn['category{}_txtHeight'.format(self._lang)]
        gv.kojimaConfig.wiseSayingPattern.speaker_ipX = srWiseSayingPtrn['speaker{}_ipX'.format(self._lang)]
        gv.kojimaConfig.wiseSayingPattern.speaker_ipY = srWiseSayingPtrn['speaker{}_ipY'.format(self._lang)]
        gv.kojimaConfig.wiseSayingPattern.speaker_fontSize = srWiseSayingPtrn['speaker{}_fontSize'.format(self._lang)]
        gv.kojimaConfig.wiseSayingPattern.speaker_indentYPoint = srWiseSayingPtrn['speaker{}_indentYPoint'.format(self._lang)]
        gv.kojimaConfig.wiseSayingPattern.speaker_txtHeight = srWiseSayingPtrn['speaker{}_txtHeight'.format(self._lang)]
        gv.kojimaConfig.wiseSayingPattern.category_label = '出典:{}' if self._lang == self.botLang.jp else 'source:{}'

    def generateTweetImage(self):
        
        """
        名言ツイート画像を生成する
        """
        
        # 名言ツイートDataFrame取得
        dfWiseSaying = self.getWiseSayingTweetData()        
        if len(dfWiseSaying):
            srWiseSayingTweet = dfWiseSaying.iloc[0]
        else:
            return ''

        # 名言ツイートパターンリストDataFrame取得
        self.getWiseSayingPtrnData(srWiseSayingTweet['pattern'])
        wsp = gv.kojimaConfig.wiseSayingPattern
        
        # イメージクラスインスタンス
        imageFileName = srWiseSayingTweet['file_name']
        orgFolderDir = gv.kojimaConfig.orgImageFolderDir
        genFolderDir = gv.kojimaConfig.genImageFolderDir
        uwi = uwImage(self.rootPathFull, imageFileName, orgFolderDir, genFolderDir)

        # フォントファイル名取得
        fontFileName = wsp.font_name
        fontFilePath = os.path.join(gv.kojimaConfig.fontFolderDir, fontFileName)

        # テキストの文字数に応じて挿入開始位置を調整
        adjInsertPointY = self.getAdjustInsertPointY(srWiseSayingTweet['wise_saying_{}'.format(self._lang)], 
                                                     wsp.say_indentYPoint, 
                                                     wsp.say_txtHeight, 
                                                     4)
        
        # テキスト挿入(本文)
        uwi.setFont(fontFilePath, wsp.say_fontSize)
        uwi.insertText(srWiseSayingTweet['wise_saying_{}'.format(self._lang)], 
                       insertPoint=(wsp.say_ipX,adjInsertPointY + wsp.say_ipY), 
                       indentationYPoint=wsp.say_indentYPoint, 
                       textHeight=wsp.say_txtHeight)

        # テキスト挿入(category)
        if srWiseSayingTweet['category_{}'.format(self._lang)] != '':
            uwi.setFont(fontFilePath, wsp.category_fontSize)
            uwi.insertText(wsp.category_label.format(srWiseSayingTweet['category_{}'.format(self._lang)]), 
                           insertPoint=(wsp.category_ipX,wsp.category_ipY), 
                           indentationYPoint=wsp.category_indentYPoint, 
                           textHeight=wsp.category_txtHeight)

        # テキスト挿入(speaker)
        if srWiseSayingTweet['speaker_{}'.format(self._lang)] != '':
            uwi.setFont(fontFilePath, wsp.speaker_fontSize)
            uwi.insertText('@{}'.format(srWiseSayingTweet['speaker_{}'.format(self._lang)]), 
                           insertPoint=(wsp.speaker_ipX,wsp.speaker_ipY), 
                           indentationYPoint=wsp.speaker_indentYPoint, 
                           textHeight=wsp.speaker_txtHeight)

        # イメージを保存する
        return uwi.saveImage()
    
    def getReplyTweetImageText(self, replyFromTweet_text):
        
        """
        返信画像に挿入する返信ツイート内容を取得

        replyFromTweet_text : str
            返信元ツイート
        """
        
        # 全国苗字データDataFrame取得
        dfLastName = self.getLastNameData()
        
        # 返信ツイートDataFrame取得
        dfReplyTweet = self.getReplyTweetData()
                
        # 返信ツイートテキストに苗字が含まれるか確認
        srLastName = self.matchingLastName(dfLastName, replyFromTweet_text)
        
        # 取得した苗字を返信ツイートパターンと照合する
        srReplyTweet = self.matchingReplyTweetTextInLastName(replyFromTweet_text, srLastName, dfReplyTweet)
        
        # 返信ツイート内容を返す
        return srReplyTweet
    
    def getLastNameData(self):
        
        """
        全国苗字データ取得
        """        

        # 基底側で取得
        dfLastName = super().getLastNameData()
        # 文字数の降順にソートする
        dfLastName['order'] = dfLastName['last_name'].apply(lambda x: len(x))
        dfLastName = dfLastName.sort_values('order', ascending=False)

        # 戻り値を返す
        return dfLastName
    
    def matchingLastName(self, dfLastName:DataFrame, replyFromTweet_text):
        
        """
        返信ツイートテキストに苗字が含まれるか確認
        マッチングされた苗字データをSeriesで返す
        
        dfLastName : DataFrame
            全国苗字データDataFrame
        replyFromTweet_text : str
            返信元ツイート            
        """
        
        srMatchedLastName = None
        
        # 全国苗字データを1件ずつループ
        for index, row in dfLastName.iterrows():
            
            if row['last_name'] in replyFromTweet_text:
            
                # マッチした行をセットする
                srMatchedLastName = row
                break
                
        return srMatchedLastName
    
    def matchingReplyTweetTextInLastName(self, replyFromTweet_text, srLastName, dfReplyTweet:DataFrame):
        
        """
        取得した苗字を返信ツイートパターンと照合する
        マッチングされた返信ツイート内容をSeriesで返す

        replyFromTweet_text : str
            返信元ツイート
        srLastName : Series
            苗字データ
        dfReplyTweet : DataFrame
            返信ツイートデータ
        """
        
        # 返却用Series初期化
        srReplyTweet = None
        
        # ワイルドカード返信ツイート抽出
        dfWildCardPattern:DataFrame = dfReplyTweet[dfReplyTweet['keyword1'].str.contains('\*')]
        
        # ワイルドカード以外の返信ツイート抽出
        dfNotWildCardPattern:DataFrame = dfReplyTweet[dfReplyTweet['keyword1'].str.contains('\*') == False]
        
        # keyword1+keyword2
        for index, row in dfNotWildCardPattern.iterrows():
            
            # 苗字が返信元ツイートに含まれるか
            if row['keyword1'] + row['keyword2'] in replyFromTweet_text:
                srReplyTweet = row
                break
            else:
                continue

        # keyword1+keyword3
        if srReplyTweet is None:
            for index, row in dfNotWildCardPattern.iterrows():
                
                # 苗字が返信元ツイートに含まれるか
                if row['keyword1'] in replyFromTweet_text or (row['keyword3'] != '' and row['keyword3'] in replyFromTweet_text):
                    srReplyTweet = row
                    break
                else:
                    continue
        
        # マッチングしなかった場合はワイルドカードのいずれかとする
        if srReplyTweet is None:

            # 苗字判定用テキストファイル読込
            lastnameTargetStrTextFilePath = os.path.join(self.rootPath, 
                                                         gv.kojimaConfig.appListDir, 
                                                         gv.kojimaConfig.lastnameTargetStrTextFileName)
            with open(lastnameTargetStrTextFilePath,'r',encoding='utf-8') as f:
                targetStr = f.read().split('\n')
            
            # 特定の文字がマッチングされた苗字に含まれるか
            if not srLastName is None:
                matchedLastName = [matchStr for matchStr in targetStr if matchStr in srLastName['last_name']]
                if len(matchedLastName) > 0:
                    # 名前が惜しい
                    srReplyTweet = dfWildCardPattern[dfWildCardPattern['keyword1'] == '*1'].iloc[0]
                else:
                    # 名前が惜しくない
                    srReplyTweet = dfWildCardPattern[dfWildCardPattern['keyword1'] == '*3'].iloc[0]
            else:
                # 返信ツイートに名前が含まれない
                srReplyTweet = dfWildCardPattern[dfWildCardPattern['keyword1'] == '*2'].iloc[0]
        
        return srReplyTweet
    
    def generateReplyTweetImage(self, srReplyTweet):

        """
        返信画像を生成する

        replyTweetText : str
            返信ツイートテキスト
        """
        
        # 返信ツイートパターンDataFrame取得
        self.getReplyTweetPtrnData(srReplyTweet['pattern'])
        wsp = gv.kojimaConfig.replyTweetPattern
        
        # イメージクラスインスタンス
        imageFileName = srReplyTweet['file_name']
        orgFolderDir = gv.kojimaConfig.orgImageFolderDir
        genFolderDir = gv.kojimaConfig.genImageFolderDir
        uwi = uwImage(self.rootPathFull, imageFileName, orgFolderDir, genFolderDir)

        # フォントファイル名取得
        fontFileName = wsp.font_name
        fontFilePath = os.path.join(gv.kojimaConfig.fontFolderDir, fontFileName)

        # テキストの文字数に応じて挿入開始位置を調整
        adjInsertPointY = self.getAdjustInsertPointY(srReplyTweet['reply_text'], 
                                                     wsp.reply_indentYPoint, 
                                                     wsp.reply_txtHeight, 
                                                     4)
        
        # テキスト挿入(本文)
        uwi.setFont(fontFilePath, wsp.reply_fontSize)
        uwi.insertText(srReplyTweet['reply_text'], 
                       insertPoint=(wsp.reply_ipX,adjInsertPointY + wsp.reply_ipY), 
                       indentationYPoint=wsp.reply_indentYPoint, 
                       textHeight=wsp.reply_txtHeight,
                       fontColor=(0,0,0))

        # イメージを保存する
        return uwi.saveImage()
