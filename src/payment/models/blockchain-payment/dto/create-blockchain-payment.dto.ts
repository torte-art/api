import { ApiProperty } from '@nestjs/swagger';
import { IsEnum, IsNotEmpty, IsNumber, IsOptional, IsString } from 'class-validator';
import { BlockchainPaymentType } from '../blockchain-payment.entity';

export class CreateBlockchainPaymentDto {
  @ApiProperty()
  @IsNotEmpty()
  @IsEnum(BlockchainPaymentType)
  type: BlockchainPaymentType;

  @ApiProperty()
  @IsNotEmpty()
  @IsString()
  command: string;

  @ApiProperty()
  @IsNotEmpty()
  @IsString()
  tx: string;

  @IsOptional()
  asset: any;

  @ApiProperty()
  @IsNotEmpty()
  @IsNumber()
  assetValue: number;
}