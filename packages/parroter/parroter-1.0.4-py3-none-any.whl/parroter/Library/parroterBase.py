import os
import sys
import math
import LibHanger.Library.uwLogger as Logger
from twython import Twython, TwythonError
from LibHanger.Library.uwImport import JsonImporter
from LibHanger.Library.uwConfig import cmnConfig
from parroter.Library.parroterConfig import parroterConfig

class parroterBase():
    
    """
    parroter基底クラス
    """
    
    class botLang():
        
        """
        言語設定
        """
        
        jp = 'Jp'
        """ 日本語 """

        en = 'En'
        """ 英語 """

    def __init__(self, rootPath, lang:str = botLang.jp) -> None:
        
        """
        コンストラクタ
        
        Parameters
        ----------
        rootPath : str
            ルートパス
        lang : str
            言語
        """

        # 言語設定
        self._lang = lang
        
        # LibHanger.ini
        dc = cmnConfig()
        dc.getConfig(rootPath)
        
        # ロガー設定
        Logger.setting(dc)

        # 共通設定
        self.config = dc
        self.parroterConfig:parroterConfig = None
        
        # キートークン初期化
        self.twitter = None
        
        # ルートパス
        self.rootPathFull = rootPath
        self.rootPath = os.path.dirname(rootPath)
    
    @property
    def appName(self):
        
        """
        アプリ名
        """

        return ''
    
    def settingLogOutputPath(self):
        
        """
        ログ出力先設定
        """
        
        # ログ出力先ディレクトリを作成
        self.hello_id_dir, self.reply_log_dir = self.createLogOutputDir()
        
        # ログ出力先取得
        self.hello_id_path, self.reply_log_path = self.getLogOutputPath(self.hello_id_dir, self.reply_log_dir)
    
    def settingConfig(self):
        
        """
        parroter共通設定(派生側でオーバーライドする)
        """
        
        pass
    
    def setKeyToken(self):
        
        """
        キートークンを設定する
        """
        
        # キートークン設定
        self.twitter = Twython(
                         self.parroterConfig.consumer_key
                        ,self.parroterConfig.consumer_secret
                        ,self.parroterConfig.access_token
                        ,self.parroterConfig.access_token_secret
                        )
    
    def tweetHello(self):
        
        """
        挨拶をツイートする
        """
        
        # 挨拶ツイート内容の設定
        helloTweetText = self.getHelloTweetText()

        # ツイートに含める画像の設定
        helloTweetImage = self.getHelloTweetImage()
                
        # 挨拶をツイートする
        response, result = self.tweet(helloTweetText, helloTweetImage)
        if result:
            
            try:
                                
                # 挨拶ツイートログ出力
                self.createHelloTweetLog(response, self.hello_id_path)
                                
            except Exception as e:                
                # エラーロギング
                Logger.logging.error(e.msg)
                # 処理を停止
                sys.exit(1)

        else:
            # 処理を停止
            sys.exit(1)
        
    def getHelloTweetText(self):
        
        """
        挨拶文を取得する
        """
        
        return ''
    
    def getHelloTweetImage(self):
        
        """
        挨拶ツイートに含める画像を取得する
        """
        
        return ''
    
    def getAdjustInsertPointY(self, insertText, indentYPoint, txtHeight, maxIndentCount):

        """
        テキスト挿入位置調整

        Parameters
        ----------
        insertText : str
            挿入文字列
        indentYPoint : int
            1行あたり文字数
        txtHeight : int
            文字高さ
        maxIndentCount : int
            最大字下げ数            
        """
                
        insertTextLen = len(insertText)
        if insertTextLen <= indentYPoint:
            adjInsertPointY = 0
        else:
            baseLength = indentYPoint * maxIndentCount
            indentCount = math.floor(baseLength / insertTextLen) if insertTextLen < baseLength else maxIndentCount
            adjInsertPointY = -1 * (txtHeight * indentCount)
        
        return adjInsertPointY
    
    def uploadImage(self, tweetImageFilePath):
        
        """
        イメージファイルをアップロードする

        Parameters
        ----------
        tweetImageFilePath : str
            イメージファイルパス        
        """
        
        # イメージファイルを開く
        image = open(tweetImageFilePath,'rb')
        # イメージファイルアップロード
        image_upl_inf = self.twitter.upload_media(media=image)
        # media_id取得
        media_id = image_upl_inf['media_id']                    

        # 戻り値を返す
        return media_id
    
    def tweet(self, tweetText, tweetImageFilePath = ''):
        
        """
        ツイートする
        
        Parameters
        ----------
        tweetText : str
            ツイート文
        tweetImageFilePath : str
            ツイート画像ファイルパス
        """
        
        response = None
        try:
            # 挨拶ツイート
            if tweetImageFilePath == '': # テキストのみ
                response = self.twitter.update_status(status=tweetText)
            else: # 画像付き
                if os.path.exists(tweetImageFilePath):
                    media_id = self.uploadImage(tweetImageFilePath)
                    response = self.twitter.update_status(status=tweetText, media_ids=[media_id])
                else:
                    response = self.twitter.update_status(status=tweetText)
        except TwythonError as e:
            # エラーロギング
            Logger.logging.error(e.msg)
            # Falseを返す
            return response, False
        else:
            return response, True
        
    def getLogOutputPath(self, hello_id_dir, reply_log_dir):
        
        """
        ログ出力先を返す

        Parameters
        ----------
        hello_id_dir : str
            挨拶ツイートIDログ出力先
        reply_log_dir : str
            返信ツイートIDログ出力先
        """
        
        # ログ出力先
        hello_id_path = os.path.join(hello_id_dir, 
                                     self.parroterConfig.hello_id_filename)
        reply_log_path = os.path.join(reply_log_dir, 
                                      self.parroterConfig.reply_log_filename)
        
        # ログ出力先を返す
        return hello_id_path, reply_log_path
    
    def createLogOutputDir(self):
        
        """
        ログ出力先ディレクトリ作成
        """

        # ログ出力先ディレクトリ
        hello_id_dir = os.path.join(self.rootPath, 
                                    self.parroterConfig.hello_id_folder)
        reply_log_dir = os.path.join(self.rootPath, 
                                     self.parroterConfig.reply_log_folder)
        
        # ログ出力先ディレクトリを作成
        os.makedirs(hello_id_dir, exist_ok=True)
        os.makedirs(reply_log_dir, exist_ok=True)
        
        # 作成したディレクトリパスを返す
        return hello_id_dir, reply_log_dir

    def createHelloTweetLog(self, response, hello_id_path):
        
        """
        挨拶ツイートログ出力

        Parameters
        ----------
        response : any
            tweet-response
        hello_id_path : str
            挨拶ツイートIDログ出力先        
        """
        
        # 挨拶ツイートログ出力
        with open(hello_id_path, mode='w') as f:
            f.write(response['id_str'])
            
    def outputReplyTweetLog(self, response, reply_log_path):
        
        """
        返信ツイートログ出力
        
        Parameters
        ----------
        response : any
            tweet-response
        reply_log_path : str
            返信ツイートIDログ出力先  
        """
        
        # 返信ツイートログ出力
        with open(reply_log_path, mode='a') as f:
            f.write(response['id_str'] + '\n')
    
    def doReply(self):
        
        """
        特定のツイートに対して返信する
        """
        
        # 返信するツイートID取得
        replyTargetTweetId = self.getHelloTweetLog(self.hello_id_path)
        
        # リプライカウンタ初期化
        replyCounter = 0
        
        for tweetId in replyTargetTweetId:
            
            # メンションを取得
            responses = self.getMentions()

            # フォロワーIDリストを取得
            follower_ids = self.getFollowerIdList()
            
            # 返信済リストを取得        
            replyTweetIdList = self.getReplyList()
            
            # 返信
            for response in responses:
                
                # フォロワー及び未返信ツイートかどうか判定
                if self.isReplyTweet(response, 
                                     follower_ids=follower_ids['ids'], 
                                     replyTweetIdList=replyTweetIdList):
                    
                    try:
                        # 返信をツイートする
                        replyResponse, result = self.replyTweet(response['id'], response['text'])
                        if result:

                            # 返信済リストにtweet_idを追記
                            self.outputReplyTweetLog(response, self.reply_log_path)

                            # リプライカウンタ++
                            replyCounter += 1
                            
                            # ログ出力
                            Logger.logging.info("reply complete. reply_tweet_id={}".format(replyResponse['id']))
                                                
                    except TwythonError as te:
                        Logger.logging.error(te.msg)
                        sys.exit(1)

            # ログ出力
            Logger.logging.info("doReply finished. reply Count={}".format(str(replyCounter)))
    
    @Logger.loggerDecorator("getting mentioins")
    def getMentions(self):
        
        """
        メンションを取得
        """
        
        responses = None
        try:
            responses = self.twitter.get_mentions_timeline(count=self.parroterConfig.mentionsGetCount)
        except TwythonError as e:
            Logger.logging.error(e.msg)
            sys.exit(1)
            
        return responses
    
    @Logger.loggerDecorator("getting follower id list")
    def getFollowerIdList(self):
        
        """
        フォロワーIDリストを取得
        """
    
        try:
            follower_ids = self.twitter.get_followers_ids(stringify_ids=True)
        except TwythonError as e:
            Logger.logging.error(e.msg)
            sys.exit(1)

        return follower_ids
    
    @Logger.loggerDecorator("getting reply id list")
    def getReplyList(self):

        """
        返信済リストを取得
        """        
        
        # 返信済リストを取得
        replyTweetIdList = []
        if os.path.exists(self.reply_log_path):
            
            with open(self.reply_log_path, mode='r', encoding='utf-8') as f:
                replyTweetIdList = f.read().split('\n')
                
        else:
            
            with open(self.reply_log_path, mode='w', encoding='utf-8') as f:
                pass
                
        return [replyTweetId for replyTweetId in replyTweetIdList if replyTweetId != '']
    
    def isReplyTweet(self, response, **kwargs):
        
        """
        返信対象ツイートか判定する

        Parameters
        ----------
        response : any
            tweet-response
        """
        
        # フォロワーリスト
        follower_ids = kwargs.get('follower_ids')
        # 返信済ツイートID
        replyTweetIdList = kwargs.get('replyTweetIdList')
        
        # 返信者のユーザーID取得
        usr_id = response['user']['id_str']
        
        # 返信対象かどうか判定結果を返す
        # フォロワーかつ返信済ツイートIDリストに含まれないツイートか
        return usr_id in follower_ids and not response['id_str'] in replyTweetIdList

    def getReplyTweetImageText(self, replyFromTweet_text):
        
        """
        返信画像に挿入するテキストを取得

        replyFromTweet_text : str
            返信されたツイートテキスト
        """
        
        pass
    
    def generateReplyTweetImage(self, replyTweetText):

        """
        返信画像を生成する

        replyTweetText : str
            返信ツイートテキスト
        """
        
        pass
    
    def replyTweet(self, replyTarget_tweet_id, replyFromTweet_text):

        """
        返信をツイートする

        replyTarget_tweet_id : str
            返信対象となるツイートID
        replyFromTweet_text : str
            返信されたツイートテキスト
        """

        replyResponse = None
        try:
            # 返信画像に挿入する返信ツイート内容を取得
            srReplyTweet = self.getReplyTweetImageText(replyFromTweet_text)

            # 返信画像を生成
            imageFilePath = self.generateReplyTweetImage(srReplyTweet)
            if imageFilePath:

                # 返信画像アップロード
                media_id = self.uploadImage(imageFilePath)
                
                # 返信をツイート
                replyResponse = self.twitter.update_status(status='',
                                                           in_reply_to_status_id=replyTarget_tweet_id, 
                                                           auto_populate_reply_metadata=True, 
                                                           media_ids=media_id)
            else:
                
                # 返信をツイート
                replyResponse = self.twitter.update_status(status=srReplyTweet['reply_text'], 
                                                           in_reply_to_status_id=replyTarget_tweet_id,
                                                           auto_populate_reply_metadata=True)

        except TwythonError as e:
            # エラーロギング
            Logger.logging.error(e.msg)
            # Falseを返す
            return replyResponse, False
        else:
            return replyResponse, True
                    
    def getHelloTweetLog(self, hello_id_path):
        
        """
        挨拶ツイートログ取得

        Parameters
        ----------
        hello_id_path : str
            挨拶ツイートIDログ出力先        
        """
        
        # 挨拶ツイートログ取得
        with open(hello_id_path, mode='r', encoding='utf-8') as f:
            return f.read().split('\n')
            
    def getLastNameData(self):
        
        """
        全国苗字データ取得
        """        
        
        # 全国苗字jsonファイルをDataFrameに変換
        ji = JsonImporter(self.rootPathFull)
        dfLastName = ji.convertToDataFrame(self.parroterConfig.lastNameJsonDir, self.parroterConfig.lastNameJsonFileName)

        return dfLastName
    
    def getReplyTweetData(self):
        
        """
        返信ツイートデータ取得
        """        
        
        # 返信ツイートjsonファイルをDataFrameに変換
        ji = JsonImporter(self.rootPathFull)
        dfReplyTweet = ji.convertToDataFrame(self.parroterConfig.replyJsonDir, self.parroterConfig.replyJsonFileName)

        return dfReplyTweet
        
    def getReplyTweetPtrnData(self, replyTweetPattern):
        
        """
        返信ツイートパターンデータ取得
        
        Parameters
        ----------
        replyTweetPattern : Series
            返信ツイートパターン        
        """        
        
        # 返信ツイートパターンjsonファイルをDataFrameに変換
        ji = JsonImporter(self.rootPathFull)
        dfReplyTweetPtrn = ji.convertToDataFrame(self.parroterConfig.replyJsonDir, self.parroterConfig.replyPtrnJsonFileName)

        # 該当する返信ツイートパターンを取得
        srReplyTweetPtrn = dfReplyTweetPtrn[dfReplyTweetPtrn['pattern'] == replyTweetPattern].iloc[0]

        # 返信ツイートパターンリストクラスへ値セット
        self.parroterConfig.replyTweetPattern.pattern = replyTweetPattern
        self.parroterConfig.replyTweetPattern.font_name = srReplyTweetPtrn['font_name']
        self.parroterConfig.replyTweetPattern.reply_ipX = srReplyTweetPtrn['reply{}_ipX'.format(self._lang)]
        self.parroterConfig.replyTweetPattern.reply_ipY = srReplyTweetPtrn['reply{}_ipY'.format(self._lang)]
        self.parroterConfig.replyTweetPattern.reply_fontSize = srReplyTweetPtrn['reply{}_fontSize'.format(self._lang)]
        self.parroterConfig.replyTweetPattern.reply_indentYPoint = srReplyTweetPtrn['reply{}_indentYPoint'.format(self._lang)]
        self.parroterConfig.replyTweetPattern.reply_txtHeight = srReplyTweetPtrn['reply{}_txtHeight'.format(self._lang)]
