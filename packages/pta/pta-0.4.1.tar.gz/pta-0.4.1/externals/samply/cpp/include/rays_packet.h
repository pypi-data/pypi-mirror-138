// Copyright (c) 2021 ETH Zurich, Mattia Gollub (mattia.gollub@bsse.ethz.ch)
// Computational Systems Biology group, D-BSSE
//
// This software is freely available under the GNU General Public License v3.
// See the LICENSE file or http://www.gnu.org/licenses/ for further information.

#ifndef SAMPLY_RAYS_PACKET_H
#define SAMPLY_RAYS_PACKET_H

#include <type_traits>

#include "commons.h"

namespace samply {

template <typename Scalar>
struct RaysPacket;

//======================================================================================
//	Storage types for ray packets.
//======================================================================================

template <typename Scalar>
struct RaysPacketStorage {
    RaysPacketStorage()
    {
    }

    RaysPacketStorage(const Matrix<Scalar>& origins, const Matrix<Scalar>& directions)
        : origins(origins), directions(directions)
    {
    }

    Matrix<Scalar> origins;
    Matrix<Scalar> directions;
};

template <typename Scalar, typename ViewFunc>
struct RaysPacketViewStorage {
    RaysPacketViewStorage(const RaysPacket<Scalar>& ray_packet,
                          const ViewFunc view_function)
        : origins(view_function(ray_packet.origins)),
          directions(view_function(ray_packet.directions))
    {
    }

    typename std::invoke_result<ViewFunc, Matrix<Scalar>>::type origins;
    typename std::invoke_result<ViewFunc, Matrix<Scalar>>::type directions;
};

//======================================================================================
//	Base class for ray packets.
//======================================================================================

template <typename Scalar, typename Storage>
struct RaysPacketBase : public Storage {
    using Storage::Storage;

    Matrix<Scalar> at(const Vector<Scalar>& t) const
    {
        return this->origins + this->directions * t.asDiagonal();
    }

    Matrix<Scalar> at(const Eigen::VectorXi& ray_indices, const Vector<Scalar>& t) const
    {
        return this->origins(Eigen::all, ray_indices) +
               this->directions(Eigen::all, ray_indices) * t.asDiagonal();
    }

    Vector<Scalar> at(const int& ray_index, const Scalar t) const
    {
        return this->origins.col(ray_index) + this->directions.col(ray_index) * t;
    }

    template <typename IndexList>
    RaysPacket<Scalar> operator()(const IndexList& ray_indices) const
    {
        return RaysPacket<Scalar>{this->origins(Eigen::all, ray_indices),
                                  this->directions(Eigen::all, ray_indices)};
    }
};

//======================================================================================
//	Rays packets classes.
//======================================================================================

template <typename Scalar>
struct RaysPacket : public RaysPacketBase<Scalar, RaysPacketStorage<Scalar>> {
    using RaysPacketBase<Scalar, RaysPacketStorage<Scalar>>::RaysPacketBase;
};

template <typename Scalar, typename ViewFunc>
struct RaysPacketView
    : public RaysPacketBase<Scalar, RaysPacketViewStorage<Scalar, ViewFunc>> {
    using RaysPacketBase<Scalar,
                         RaysPacketViewStorage<Scalar, ViewFunc>>::RaysPacketBase;
};

}  // namespace samply

#endif