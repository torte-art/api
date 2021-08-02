import {
    Entity,
    PrimaryGeneratedColumn,
    Column,
    PrimaryColumn,
    Index,
    CreateDateColumn,
  } from 'typeorm';
  import * as typeorm from 'typeorm';
  
  @Entity()
  export class Language {
    @PrimaryGeneratedColumn()
    id: number;
  
    @Column({ type: 'varchar', unique: true, length: 4 })
    symbol: string;
  
    @Column({ type: 'varchar', length: 34 })
    name: string; 

    @Column({ type: 'varchar', length: 34 })
    foreignName: string; 
  
    @Column({ default: 1 })
    enable: boolean;
  
    @CreateDateColumn() 
    created: Date;
  }
  