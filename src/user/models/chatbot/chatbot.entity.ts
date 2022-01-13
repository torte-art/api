import { Column, Entity, JoinColumn, OneToOne, PrimaryGeneratedColumn } from 'typeorm';
import { UserData } from '../userData/userData.entity';

@Entity()
export class Chatbot {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ length: 256 })
  url: string;

  @Column({ length: 256 })
  version: string;

  @Column({ nullable: true })
  result: string;

  @OneToOne(() => UserData, { nullable: false })
  @JoinColumn()
  userData: UserData;
}
