import { Entity, PrimaryGeneratedColumn, Column, PrimaryColumn, OneToMany } from 'typeorm';

@Entity({
  name: 'users',
})
export class User {
  @PrimaryColumn({ type: 'varchar', length: 34, unique: true })
  address: string;

  @PrimaryGeneratedColumn({ type: 'int' })
  ref: number;

  @Column({ type: 'varchar', unique: true, length: 88 })
  signature: string;

  @Column({ type: 'varchar', length: 64, default: '' })
  mail: string;

  @Column({ type: 'int', default: 0 })
  // @ManyToOne((_type) => )
  walletId: number; //TODO: Objekt Referenzieren

  @Column({ type: 'int', default: 0 })
  usedRef: number;

  @Column({ type: 'varchar', length: 64, default: '' })
  firstname: string;

  @Column({ type: 'varchar', length: 64, default: '' })
  surname: string;

  @Column({ type: 'varchar', length: 64, default: '' })
  street: string;

  @Column({ type: 'varchar', length: 5, default: '' })
  houseNumber: string;

  @Column({ type: 'varchar', length: 64, default: '' })
  location: string;

  @Column({ type: 'varchar', length: 9, default: '' })
  zip: string;

  @Column({ type: 'varchar', length: 3, default: '' })
  country: string;

  @Column({ type: 'varchar', length: 15, default: '' })
  phone: string;
}