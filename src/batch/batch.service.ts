import { Injectable } from '@nestjs/common';
import { CreateBatchDto } from 'src/batch/dto/create-batch.dto';
import { BatchRepository } from 'src/batch/batch.repository';
import { UpdateBatchDto } from './dto/update-batch.dto';

@Injectable()
export class BatchService {
  constructor(private batchRepository: BatchRepository) {}

  async createBatch(createBatchDto: CreateBatchDto): Promise<any> {
    return this.batchRepository.createBatch(createBatchDto);
  }

  async getAllBatch(): Promise<any> {
    return this.batchRepository.getAllBatch();
  }

  async updateBatch(batch: UpdateBatchDto): Promise<string> {
    return this.batchRepository.updateBatch(batch);
  }

  async getBatch(key: any): Promise<any> {
    return this.batchRepository.getBatch(key);
  }
}