import { Injectable } from '@nestjs/common';
import { LogRepository } from './log.repository';
import { CreateLogDto } from './dto/create-log.dto';
import { MailService } from 'src/services/mail.service';
import { CreateVolumeLogDto } from './dto/create-volume-log.dto';
import { HttpService } from 'src/shared/services/http.service';
import { LogDirection, LogType } from './log.entity';
import { UserRepository } from 'src/user/user.repository';
import { User } from 'src/user/user.entity';
import { AssetService } from 'src/shared/models/asset/asset.service';
import { FiatService } from 'src/shared/models/fiat/fiat.service';

@Injectable()
export class LogService {
  constructor(
    private logRepository: LogRepository,
    private mailService: MailService,
    private http: HttpService,
    private assetService: AssetService,
    private fiatService: FiatService,
    private userRepo: UserRepository,
  ) {}
  private readonly baseUrl = 'https://api.coingecko.com/api/v3/coins/defichain/market_chart?vs_currency=chf&days=1';

  async createLog(createLogDto: CreateLogDto): Promise<any> {
    return this.logRepository.createLog(createLogDto, this.assetService, this.fiatService, this.mailService);
  }

  async createVolumeLog(createLogDto: CreateVolumeLogDto): Promise<any> {
    let assetObject = null;
    let fiatObject = null;

    if (createLogDto.payment) {
      // if (createLogDto.direction === LogDirection.fiat2asset) {
      // TODO: re-enable
      //   createLogDto.payment =
      //     createLogDto.direction === LogDirection.fiat2asset
      //       ? await this.buyPaymentRepo.getPaymentInternal(createLogDto.payment)
      //       : await this.sellPaymentRepo.getPaymentInternal(createLogDto.payment);
      // } else {
      //   createLogDto.payment = await this.sellPaymentRepo.getPaymentInternal(createLogDto.payment);
      // }
    } else {
      delete createLogDto.payment;
    }

    if (createLogDto.fiat) {
      fiatObject = await this.fiatService.getFiat(createLogDto.fiat);
    } else {
      delete createLogDto.fiat;
    }

    if (createLogDto.asset) {
      assetObject = await this.assetService.getAsset(createLogDto.asset);
    }

    if (assetObject.name != 'DFI') {
      assetObject = await this.assetService.getAsset('DFI');

      const result = await this.http.get(`${this.baseUrl}`);
      const resultArray = result['prices'];

      let sumPrice = 0;
      for (const price of resultArray) {
        sumPrice += Number.parseFloat(price[1]);
      }

      const currentDfiPrice = sumPrice / resultArray.length;

      const volumeInDFI = createLogDto.fiatInCHF / currentDfiPrice;

      createLogDto.assetValue = volumeInDFI;
    }

    if (fiatObject) createLogDto.fiat = fiatObject.id;
    if (assetObject) createLogDto.asset = assetObject.id;

    createLogDto.type = LogType.VOLUME;

    createLogDto.orderId = createLogDto.address + ':' + new Date().toISOString();

    if (!createLogDto.user) {
      const userObject = await this.userRepo.getUserInternal(createLogDto.address);

      createLogDto.user = userObject;
      createLogDto.message = userObject.usedRef;
    }

    delete createLogDto.address;

    const log = await this.logRepository.createVolumeLog(createLogDto);

    log.asset = assetObject;
    log.fiat = fiatObject;

    return log;
  }

  async getAllLog(): Promise<any> {
    return this.logRepository.getAllLog();
  }

  async getAllUserLog(address: string): Promise<any> {
    return this.logRepository.getAllUserLog(address);
  }

  async getLog(key: any): Promise<any> {
    return this.logRepository.getLog(key);
  }

  async getRefVolume(ref: string): Promise<any> {
    return this.logRepository.getRefVolume(ref);
  }

  async getAssetVolume(logType: LogType, logDirection: LogDirection): Promise<any> {
    return this.logRepository.getAssetVolume(logType, logDirection);
  }

  async getChfVolume(logType: LogType, logDirection: LogDirection): Promise<any> {
    return this.logRepository.getChfVolume(logType, logDirection);
  }

  async getUserVolume(user: User, logDirection: LogDirection): Promise<any> {
    return this.logRepository.getUserVolume(user, logDirection);
  }
}
